# Day 0: the requests that need a person, ready to send

For [issue #260](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/260), PR 294 round 3 (2026-11-28).

**Why this folder exists:** the PR listed as not done that "nothing is bought, built, quoted by a person, or reviewed
by BYU's LSO or EHS". Those steps need people. This folder makes them a morning's work:
- it lists what each office and each seller needs from us, with the numbers;
- it lists what to ask them.

**Status:** nothing here has been sent. BYU's laser-safety and radiation-safety pages redirect to a BYU sign-in, and so
do their archived copies. So the forms themselves are not known; this folder holds the content any such form asks for.

**Who sends them:** the requests below are for whoever Sterling names on day 0. Sending them needs a BYU account and
a person; an agent can't do it.

## 1. BYU's laser safety program (the LSO's office)

**Send:**
- the machine's description;
- §1.1, the data;
- §1.2's interlocks;
- the hazard numbers in [`lso-numbers.md`](lso-numbers.md) (`lso_numbers.py`: PR 266's method, FT-1's inputs).

**Ask for:**
- the registration form;
- the SOP template;
- whether they will treat the closed machine as Class 1 in operation;
- the alignment rules;
- the eyewear;
- the training;
- whether the room needs to be a controlled area.

### 1.1 The laser and the beam path

| Item | Value | Source |
|---|---|---|
| Laser | used IPG YLR-400-SM-EOS, CW fibre laser, 1070 nm, 400 W, single-mode (M² < 1.1), made Feb 2015 | `../parts.csv` L1; rating label in the listing photos |
| Classification | Class 4 | |
| Guide laser | IPG's red guide laser (for alignment) | IPG YLR user guide (`../control/README.md`) |
| Beam delivery | fibre to a 5 mm collimator, then a SCANLAB hurrySCAN 25 galvo head (2003), then a LINOS f = 254 mm f-theta objective. From there an interlocked tube runs to a window in the enclosure's lid, then a cover slide, then the build plate | study README §3.1 |
| Spot, peak irradiance | 76 µm, 1.8 × 10⁷ W/cm² | `lso-numbers.md` |
| Enclosure | Saginaw SCE-16EL1208SSLP, 304 stainless (1.9 mm), with no viewing window: a camera looks through its own window in the lid. The beam is enclosed from the fibre to the plate | `../cad/`, study README §3.7 |
| Scan field | Ø40 mm plate. The lens axis is offset 30 mm from the plate's centre, so the specular return misses the fibre | `../process/README.md` |

### 1.2 Interlocks and safe state

These are from `../control/README.md` §2 and `io-list.csv`:
- **Switches:** one Omron D4NS-2CF direct-opening tongue switch on the lid, one on the beam tube, an E-stop and a key switch.
- **Stray-beam backstop:** four normally closed 75 °C bimetal switches (Sensata 67L075), on the beam tube and the window ring.
- **Safety relay:** all of these run into an Omron G9SE-201 safety relay. Its two outputs open the laser's two hardware interlock loops. A relay on its auxiliary output pulls the scan card's /STOP input, so the list stops in hardware.
- **Software:** it can only request emission.
- **Checked:** a contact-level model of the chain never emits with a contact open, over 1,048,576 transitions.
- **Emission lamp:** on the frame.
- **Service and alignment are Class 4:** guard open, guide laser first, then the lowest stable power with a beam block, in a controlled area with eyewear. The eyewear OD at 1070 nm is ≥ 5.3 for the direct beam and ≥ 4.3 for 40 W alignment (`lso-numbers.md`). The LSO sets the actual rating and the eyewear.

## 2. EHS and the Fire Marshal's office: aluminium powder and argon

**Send:** the powder plan, from the study's §3.7 and PR 266's [`safety.md`](../../safety.md) §5 and §7:
- AlSi10Mg first, then 6061 and 7075;
- a small inventory, loaded in a glovebox;
- the box and stages bonded to ground;
- the HEPA element bagged out under argon;
- a Class D extinguisher;
- a respirator when the lid is opened after a build.

**Argon:**
- the machine holds ~24 L of gas;
- the supply is one cylinder, which is the hazard (PR 266 `safety.md` §5.1);
- a room O₂-deficiency monitor (Macurco OX-6), and the exhaust to the building exhaust.

**Ask:**
- for a dust hazard analysis and which edition of NFPA 484/652/660 applies;
- whether a UL 2011 field evaluation is needed;
- for the powder storage limits;
- for the respirator program and fit testing;
- where the O₂ monitor and the cylinder go.

## 3. Physical Facilities: the laser's circuit

**Request:** a dedicated 208/240 V, 15 A two-pole circuit at the machine's bench.
- The laser's label reads 1/N/PE 200–240 VAC, 10 A.
- The receptacle depends on the laser's cord. Check the cord on arrival, and let the electrician choose.
- Everything else (~440 W) runs on one 120 V 20 A circuit. A chiller, if the scan head needs one, would be a third circuit.
- Source: `../control/README.md` §3, `power-budget.csv`.

## 4. Questions for sellers and makers, before paying

| To | Ask | Why |
|---|---|---|
| The laser's eBay seller, and IPG with the serial number | Does this unit have back-reflection protection or a back-reflection sensor? What are its hours? Does a test log exist? Which collimator does it have, and what is its beam diameter? | Edison's top risk (study §6.1), `../process/` |
| The hurrySCAN 25's seller | Does the head's correction table or calibration sheet come with it? Is it water-cooled, and is the aperture as listed? | `../control/README.md` §6 |
| The RTC4's seller | Does the card come with its driver package and any `.ctb` files? | `../control/README.md` §6. SCANLAB's public RTC4 package (2023-11-02) already has the 64-bit DLL and the x64 driver |
| SCANLAB | correXion for this head and lens, from a burned grid | study README §3.2 |
| Ideal Vacuum (FT-1V only) | the drawing of P107540, the 12 in. cube frame, with its face opening | the deck needs ≥ 247 mm (`../cad/README.md`). The opening isn't published; the estimate is 250–260 mm (`../live-reads-2026-11-28-notes.md`) |
| Zaber | the X-LSM100B's acceleration limit, which is not published | the recoat time (`../process/README.md`) |
| BYU Purchasing | Can eBay listings go on a purchasing card? No public page says. | the used laser chain is on eBay |

**Card limits on BYU's public pages**, from `../live-reads-2026-11-28.csv` (read 2026-11-28):
- **Per purchase:** "up to $3,500". Raises "will not be approved", and split transactions are prohibited. Over $3,500, "Create a Workday requisition instead".
- **Per month:** $10,000 on an individual card, $20,000 on a department custodian card.
- **What that means for FT-1:** its card purchases come to about $29k at high prices (`../fast_track.py`). Plan the day-0 orders across more than one card, or put some vendors on a Workday requisition.

## 5. BYU's metal-AM lab

**Ask:**
- for their Class 4 SOP and their dust hazard analysis, as templates;
- whether their Concept Laser M2 takes a reduced-build-volume insert (alternative G in the study's §2).
