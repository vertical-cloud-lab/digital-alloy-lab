// Re-runs the DTSA-II quantification of the caliber#35 spectra, headless.
//
// It drives NIST's EPQ library (the engine inside DTSA-II) the way DTSA-II's
// quantification wizard and its Jython multiQuant() do: one QuantifyUsingStandards
// per beam energy, the standards act as their own references, filter fit with
// the variable-width filter, then XPP ("Pouchou & Pichoir Simplified
// (Non-normal)") and the default MAC set. See README.md in this folder.
//
// Usage (run.sh does all this):
//   java --enable-preview -cp <epq.jar + deps> RerunDTSA2.java <raw dir> <out dir> <config> [options]
// Options:
//   --fwhm <eV>           detector FWHM at Mn Ka (default 128)
//   --mg-std MgO|Mg       what the Mg row's MgO spectrum is entered as (default MgO)
//   --pure-mg-runs a,b    enter it as pure Mg for these unknowns only (as the student did)
//   --runs a,b,c          only these unknowns
//   --broaden-to <eV>     for unknowns with this amp time, convolve the standards
//   --amp <us>            with a Gaussian so their FWHM at Mn Ka becomes <eV>
//   --unk-extra <eV>      also convolve every unknown with a Gaussian of this FWHM
//                         (a self-check: see README.md)
//
// Writes <out>/<config>.csv (one row per unknown) and <out>/<config>.html (DTSA-II's
// own results table, QuantifyUsingStandards.tabulateResults()).

import gov.nist.microanalysis.EPQLibrary.*;
import gov.nist.microanalysis.EPQLibrary.Detector.*;
import gov.nist.microanalysis.EPQLibrary.RegionOfInterestSet.RegionOfInterest;
import gov.nist.microanalysis.EPQTools.SpectrumFile;
import gov.nist.microanalysis.Utility.UncertainValue2;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class RerunDTSA2 {

   static final Element[] ELMS = {Element.O, Element.Mg, Element.Al, Element.Si};

   static final String[] UNKNOWNS = {"sobol_exp_1_1", "sobol_exp_2_1", "sobol_exp_3_1", "sobol_exp_4_1", "sobol_exp_5_1",
         "sobol_exp_6_1", "trial6_1", "trial8_1", "trial9_1", "trial10_1", "trial11_1", "trial12_1", "trial13_1", "trial14_1",
         "trial15_1", "trial16_1", "trial17_1"};

   static ISpectrumData load(Path p, EDSDetector det) throws Exception {
      final ISpectrumData[] specs = SpectrumFile.open(p.toFile());
      final ISpectrumData s = specs[0];
      s.getProperties().setDetector(det);
      return s;
   }

   static String header(Path p, String key) throws IOException {
      for (String line : Files.readAllLines(p, StandardCharsets.ISO_8859_1))
         if (line.startsWith(key))
            return line.substring(line.indexOf(':') + 1).trim();
      return "";
   }

   // Convolve a spectrum with a Gaussian of constant FWHM (eV). Under EPQ's line-width
   // model, FWHM(E)^2 = FWHM_MnKa^2 + 2.45 (E - E_MnKa), so taking a detector from
   // FWHM_MnKa = f0 to f1 is a constant extra width sqrt(f1^2 - f0^2) at every energy.
   static ISpectrumData broaden(ISpectrumData src, double extraFwhmEv) {
      final EditableSpectrum res = new EditableSpectrum(src);
      final double w = src.getChannelWidth();
      final double sigCh = extraFwhmEv / 2.354820045 / w;
      final int half = (int) Math.ceil(5.0 * sigCh);
      final double[] k = new double[2 * half + 1];
      double sum = 0.0;
      for (int i = -half; i <= half; ++i)
         sum += (k[i + half] = Math.exp(-0.5 * (i / sigCh) * (i / sigCh)));
      for (int i = 0; i < k.length; ++i)
         k[i] /= sum;
      final int n = src.getChannelCount();
      for (int ch = 0; ch < n; ++ch) {
         double acc = 0.0;
         for (int i = -half; i <= half; ++i) {
            final int j = ch - i;
            if (j >= 0 && j < n)
               acc += k[i + half] * src.getCounts(j);
         }
         res.setCounts(ch, acc);
      }
      res.getProperties().setTextProperty(SpectrumProperties.SpecimenDesc,
            "broadened by " + String.format(Locale.ROOT, "%.1f", extraFwhmEv) + " eV");
      return res;
   }

   static String f(double d, int digits) {
      if (Double.isNaN(d))
         return "";
      return String.format(Locale.ROOT, "%." + digits + "f", d);
   }

   public static void main(String[] args) throws Exception {
      final Path raw = Paths.get(args[0]);
      final Path out = Paths.get(args[1]);
      final String config = args[2];
      double fwhm = 128.0;
      String mgStd = "MgO";
      Set<String> only = null;
      double broadenTo = Double.NaN;
      String broadenAmp = null;
      double unkExtra = 0.0;
      Set<String> pureMgRuns = Set.of();
      for (int i = 3; i < args.length; ++i) {
         switch (args[i]) {
            case "--fwhm" -> fwhm = Double.parseDouble(args[++i]);
            case "--mg-std" -> mgStd = args[++i];
            case "--runs" -> only = new LinkedHashSet<>(Arrays.asList(args[++i].split(",")));
            case "--broaden-to" -> broadenTo = Double.parseDouble(args[++i]);
            case "--amp" -> broadenAmp = args[++i];
            case "--unk-extra" -> unkExtra = Double.parseDouble(args[++i]);
            case "--pure-mg-runs" -> pureMgRuns = new HashSet<>(Arrays.asList(args[++i].split(",")));
            default -> throw new IllegalArgumentException(args[i]);
         }
      }
      Files.createDirectories(out);

      // DTSA-II's defaults, as in the student's report.
      final Strategy strat = new Strategy();
      strat.addAlgorithm(CorrectionAlgorithm.class, CorrectionAlgorithm.XPPExtended);
      strat.addAlgorithm(MassAbsorptionCoefficient.class, MassAbsorptionCoefficient.Default);
      AlgorithmUser.applyGlobalOverride(strat);

      final Composition mgo = MaterialFactory.createCompound("MgO");
      final Composition pureMg = MaterialFactory.createPureElement(Element.Mg);
      final Composition pureAl = MaterialFactory.createPureElement(Element.Al);
      final Composition pureSi = MaterialFactory.createPureElement(Element.Si);
      final Composition defaultMgComp = mgStd.equals("Mg") ? pureMg : mgo;

      // Group unknowns by beam energy.
      final TreeMap<Integer, List<String>> byKv = new TreeMap<>();
      for (String u : UNKNOWNS) {
         if (only != null && !only.contains(u))
            continue;
         final int kv = (int) Math.round(Double.parseDouble(header(raw.resolve("unknowns/" + u + ".msa"), "#BEAMKV")));
         byKv.computeIfAbsent(kv, k -> new ArrayList<>()).add(u);
      }

      final StringBuilder csv = new StringBuilder();
      csv.append("run,config,beam_kV,amp_time_us,detector_fwhm_MnKa_eV,standards_broadened_by_eV,mg_standard_entered_as,take_off_deg");
      for (Element e : ELMS)
         csv.append(",roi_" + e.toAbbrev() + "_keV");
      for (Element e : ELMS)
         csv.append(",k_" + e.toAbbrev() + ",k_" + e.toAbbrev() + "_sd");
      for (Element e : ELMS)
         csv.append(",Z_" + e.toAbbrev() + ",A_" + e.toAbbrev() + ",F_" + e.toAbbrev());
      for (Element e : ELMS)
         csv.append("," + e.toAbbrev() + "_wt,").append(e.toAbbrev() + "_sd");
      csv.append(",analytical_sum,analytical_sum_sd");
      for (Element e : ELMS)
         csv.append("," + e.toAbbrev() + "_wt_norm,").append(e.toAbbrev() + "_norm_sd");
      csv.append(",warning\n");

      final StringBuilder html = new StringBuilder();
      html.append("<html><head><meta charset=\"utf-8\"><title>DTSA-II re-run: " + config + "</title></head><body>\n");
      html.append("<h1>DTSA-II (EPQ " + System.getProperty("epq.version", "?") + ") re-run: " + config + "</h1>\n");
      html.append("<p>Correction: " + CorrectionAlgorithm.XPPExtended.getName() + "; MACs: "
            + MassAbsorptionCoefficient.Default.getName() + "; detector FWHM at Mn Ka " + fwhm + " eV; Mg/O standard entered as "
            + defaultMgComp.toString() + (pureMgRuns.isEmpty() ? "" : " (pure Mg for " + pureMgRuns + ")") + ".</p>\n");

      for (Map.Entry<Integer, List<String>> me : byKv.entrySet()) {
         final int kv = me.getKey();
         // One detector per configuration; the broadened path uses a broader detector for
         // the short-amp-time unknowns.
         final List<String> runs = me.getValue();
         final Map<String, List<String>> byDet = new LinkedHashMap<>();
         for (String u : runs) {
            final String amp = header(raw.resolve("unknowns/" + u + ".msa"), "##AmpTime");
            final boolean br = broadenAmp != null && amp.equals(broadenAmp) && !Double.isNaN(broadenTo);
            final boolean pm = pureMgRuns.contains(u) || defaultMgComp == pureMg;
            byDet.computeIfAbsent((br ? "broad" : "native") + (pm ? "/Mg" : "/MgO"), k -> new ArrayList<>()).add(u);
         }
         for (Map.Entry<String, List<String>> de : byDet.entrySet()) {
            final boolean br = de.getKey().startsWith("broad");
            final boolean pm = de.getKey().endsWith("/Mg");
            final Composition mgStdComp = pm ? pureMg : mgo;
            final double detFwhm = br ? broadenTo : fwhm;
            final double extra = br ? Math.sqrt(broadenTo * broadenTo - fwhm * fwhm) : 0.0;
            final EDSDetector det = EDSDetector.createSDDDetector(4096, 5.0, 0.0, detFwhm);
            // The O and Mg rows get separate copies of the MgO spectrum, as in the wizard, so that
            // entering the Mg row as pure Mg doesn't also change the O row's material.
            ISpectrumData mgoSpec = load(raw.resolve("standards/MgO_" + kv + "kV.msa"), det);
            ISpectrumData mgoSpecMg = load(raw.resolve("standards/MgO_" + kv + "kV.msa"), det);
            ISpectrumData alSpec = load(raw.resolve("standards/Al_" + kv + "kV.msa"), det);
            ISpectrumData siSpec = load(raw.resolve("standards/Si_" + kv + "kV.msa"), det);
            if (br) {
               mgoSpec = broaden(mgoSpec, extra);
               mgoSpecMg = broaden(mgoSpecMg, extra);
               alSpec = broaden(alSpec, extra);
               siSpec = broaden(siSpec, extra);
               for (ISpectrumData s : List.of(mgoSpec, mgoSpecMg, alSpec, siSpec))
                  s.getProperties().setDetector(det);
            }
            final QuantifyUsingStandards qus = new QuantifyUsingStandards(det, ToSI.keV(kv), false, true);
            qus.setOFudge(false);
            qus.addStandard(Element.O, mgo, Collections.emptySet(), mgoSpec);
            qus.addStandard(Element.Mg, mgStdComp, Collections.emptySet(), mgoSpecMg);
            qus.addStandard(Element.Al, pureAl, Collections.emptySet(), alSpec);
            qus.addStandard(Element.Si, pureSi, Collections.emptySet(), siSpec);

            final List<ISpectrumData> done = new ArrayList<>();
            for (String u : de.getValue()) {
               final Path up = raw.resolve("unknowns/" + u + ".msa");
               ISpectrumData unk = load(up, det);
               if (unkExtra > 0.0) {
                  unk = broaden(unk, unkExtra);
                  unk.getProperties().setDetector(det);
               }
               final QuantifyUsingStandards.Result res = qus.compute(unk);
               done.add(unk);
               final Composition comp = res.getComposition();
               final SpectrumProperties sp = unk.getProperties();
               final KRatioSet krs = sp.getKRatioWithDefault(SpectrumProperties.KRatios, null);
               final double toa = Math.toDegrees(SpectrumUtils.getTakeOffAngle(SpectrumUtils.applyEDSDetector(det, unk).getProperties()));
               csv.append(u).append(',').append(config).append(',').append(kv).append(',')
                     .append(header(up, "##AmpTime")).append(',').append(f(detFwhm, 1)).append(',').append(f(extra, 1)).append(',')
                     .append(pm ? "pure Mg" : "MgO").append(',').append(f(toa, 2));
               for (Element e : ELMS) {
                  final StringBuilder r = new StringBuilder();
                  for (RegionOfInterest roi : qus.getStandardROIS(e)) {
                     if (r.length() > 0)
                        r.append(' ');
                     r.append(f(FromSI.keV(roi.lowEnergy()), 3)).append('-').append(f(FromSI.keV(roi.highEnergy()), 3));
                  }
                  csv.append(',').append(r);
               }
               for (Element e : ELMS) {
                  UncertainValue2 k = null;
                  for (XRayTransitionSet xrts : krs.getTransitions())
                     if (xrts.getElement().equals(e))
                        k = krs.getKRatioU(xrts);
                  csv.append(',').append(k == null ? "" : f(k.doubleValue(), 5)).append(',').append(k == null ? "" : f(k.uncertainty(), 5));
               }
               for (Element e : ELMS) {
                  double[] zaf = null;
                  for (XRayTransitionSet xrts : krs.getTransitions())
                     if (xrts.getElement().equals(e) && comp.containsElement(e))
                        try {
                           zaf = qus.zaf(comp, xrts, sp.clone());
                        } catch (EPQException ex) {
                           zaf = null; // element culled from the result
                        }
                  csv.append(',').append(zaf == null ? ",," : f(zaf[0], 4) + "," + f(zaf[1], 4) + "," + f(zaf[2], 4));
               }
               for (Element e : ELMS) {
                  final UncertainValue2 w = comp.weightFractionU(e, false);
                  csv.append(',').append(f(100 * w.doubleValue(), 3)).append(',').append(f(100 * w.uncertainty(), 3));
               }
               final UncertainValue2 tot = comp.sumWeightFractionU();
               csv.append(',').append(f(tot.doubleValue(), 4)).append(',').append(f(tot.uncertainty(), 4));
               for (Element e : ELMS) {
                  final UncertainValue2 w = comp.weightFractionU(e, true);
                  csv.append(',').append(f(100 * w.doubleValue(), 3)).append(',').append(f(100 * w.uncertainty(), 3));
               }
               final String warn = res.getWarningMessage();
               csv.append(',').append(warn == null ? "" : '"' + warn.replace('"', '\'').replace('\n', ' ') + '"').append('\n');
               System.out.println(config + " " + u + " " + kv + " kV: " + comp.weightPercentString(false) + "  sum=" + f(tot.doubleValue(), 4));
            }
            html.append("<h2>" + kv + " kV" + (br ? ", standards broadened by " + f(extra, 1) + " eV, detector " + f(detFwhm, 1) + " eV" : "")
                  + (pm ? ", Mg standard entered as pure Mg" : "") + "</h2>\n");
            html.append(qus.tabulateResults(done, out.toFile(), Collections.emptyList()));
            html.append("\n");
         }
      }
      html.append("</body></html>\n");
      Files.writeString(out.resolve(config + ".csv"), csv.toString());
      // Point the spectrum links at the files in this repo instead of absolute paths.
      final String relRaw = out.toAbsolutePath().normalize().relativize(raw.toAbsolutePath().normalize()) + "/";
      final String page = html.toString().replace("file:" + raw.toAbsolutePath() + "/", relRaw)
            .replace("file:" + raw.toAbsolutePath().normalize() + "/", relRaw);
      Files.writeString(out.resolve(config + ".html"), page);
   }
}
