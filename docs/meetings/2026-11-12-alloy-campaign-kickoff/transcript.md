# Alloy campaign kickoff, 2026-11-12 (excerpt)

The planning meeting for the new alloy discovery campaign,
[digital-alloy-lab#255](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/255), recorded on Sterling's
phone at 1:07 PM on 2026-11-12. Gage wrote the issue during the meeting.

**The recording stops at 14:10.** The file is 48 minutes long, but it has no sound after 14:09.6, and none from 07:12
to 07:29. So this covers the first 14 minutes only. Issue 255's notes and action items cover parts of the meeting
that the recording doesn't.

**This is an excerpt.** It starts at 03:00, and two short passages after that are left out. Each cut is marked
`[...]`. A vendor contact is called "the 3D Powder Tech contact" instead of by name.

Transcribed with Whisper `large-v3` in two passes (with and without voice-activity filtering), then corrected for
sense and context. Speaker labels are inferred from what is said, not from diarization: `(?)` marks a guess, and a
short reply may be on the wrong person. Square brackets are words added for sense or best guesses at garbled words.
Where the two passes disagree, the other reading is in parentheses. Every issue, PR or comment that someone refers
to is linked inline and listed in the table at the end.

Who is there, going by issue 255 and the talk: Sterling Baird; Gage Erickson (`@gage-erickson`), writing issue 255
as they go; Carl Robison (`@carl-robison`), on printers; Xavier Zaitzeff (`@XZaitzeff`), on Thermo-Calc; and a
student on composition measurement, probably Ronnie Guymon (`@ronnie-guymon`), who runs the SEM-EDS work in
[caliber](https://github.com/vertical-cloud-lab/caliber).

---

## 03:00-07:41 A desktop LPBF printer

*[...] (00:00-03:00 left out)*

- **[03:00] Student (?):** Not to get [myself] too excited, but you said maybe bringing in a
  [desktop laser powder bed fusion system](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/245)?
- **[03:07] Sterling:** Yeah, [...]
- **[03:13] Student (?):** Oh, interesting. That'd be sweet. Would that be just a tiny one, so...?
- **[03:18] Sterling:** Smaller build plate, yeah. Or, like, it's not the big industrial [ones].
- **[03:24] Student (?):** So it'd sit on a table? Refrigerator size?
- **[03:27] Sterling:** Mini-fridge size.
- **[03:31] Sterling:** So Carl, if I could kind of
  [put you back on that](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353364974)
  too. Like, if we were to buy one that's like [$50,000](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/39),
  it's kind of maybe the budget. It's probably the budget. Is that reasonable?
- **[03:49] Carl:** It's like... It's on the lower end. But we'll definitely lose build plate size. It'll just be
  [small]. Is that important?
- **[04:00] Sterling:** We're doing mechanical testing. We could do corrosion, we could do density. We won't be
  able to do [tensile tests in an accepted form](https://github.com/vertical-cloud-lab/byu-vcl/issues/46). We could
  do... That's where we could do lots of experiments. How deep? I mean, because if the build plate's only like two
  inch by two inch, and then it's like 300 millimeters [tall]...
- **[04:24] Carl:** A lot of times the volume itself is just kind of like, yeah, that big.
- **Sterling:** Oh, really?
- **Carl:** On the [desktop ones](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353368469)
  they'd be, like, comparable to the size of, like, a baseball, kind of thing. Yeah, it's what I've seen.
- **[04:35] Sterling:** Which could be okay. We also need to make sure the laser power is enough to sufficiently
  melt it. If we have a heated build plate... Heated build plates are pretty important for
  [aluminum that can be susceptible to cracking](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/153d256/equipment/printer-survey/lpbf-options.md#4-physics-why-al-is-hard-in-lpbf-and-what-is-needed).
  Hot cracking is what they call it. It cools down and then it gets heated. So there's going to be this delta, this
  difference between doing something on one of these miniaturized printers and going to the
  [University of Utah](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/138). But that is a...
- **[05:18] Carl:** I think I could also kind of... [The 3D Powder Tech contact](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353365861)
  comes back. He's come back to mind a couple of times. He's there; he's in the back pocket. And at first I
  thought, oh, like, he did kind of
  [struggle working with that powder](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353366661).
  But we've also been struggling with that powder [in some different contexts], and he did find something that did
  get a print, and the [print came back to us](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353366838),
  and it wasn't gorgeous, but it was there.
- **Sterling (?):** Yeah, it was there.
- **[05:57] Carl:** And it's something that we could... And that's affordable enough, and that sounds scarily like
  what we're looking for. And it's really hard, because there's not a lot of companies out there that I've found
  that make something like that, that would be that customizable, in terms of, like, we could probably just kind of
  hack it ourselves.
- **[06:15] Carl:** For context, [he] is in a lab in
  [Wisconsin](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353366142), where
  he's basically creating his own laser powder bed fusion system from scratch, from very little parts. Essentially
  like what we did with the [unclear] (pass 1: "the PowerGhost airplane"; pass 2: "the power go circle plane").
- **[06:32] Sterling:** Is that what you're talking about, a
  [frugal twin](https://github.com/vertical-cloud-lab/byu-vcl/issues/214#issuecomment-5670012142)?
- **[06:35] Carl:** It's definitely that spirit, yeah, kind of like an affordable option of that. But it is pretty
  new, I would say; the first thing [was] within like the last year or so. So it's risky in the sense that there's
  just so many unknowns, but, like, it exists.
- **[06:55] Sterling:** Yeah. Um, so maybe another... Let me actually... [...]
- *[07:12-07:29: no audio]*
- **[07:28] Carl:** We were looking at a little bit
  [bigger build plates](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353365218),
  a little bit more of an expensive machine. But I'll redial that search in and see what I come up with.

## 07:41-08:03 Follow-ups on Thermo-Calc and the printer

- **[07:41] Sterling:** And then I'll plan on reaching back out to both of you about Thermo-Calc and this
  particular purchase.
- **[07:54] Xavier (?):** And then I will get back to you on
  [what BYU is going to charge us](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/141).
- **[07:58] Sterling:** That would be great.

## 08:03-10:36 The goal: beat AlSi10Mg, or match Scalmalloy with fewer critical minerals

- **[08:03] Gage:** So, two base alloys:
  [AlSi10Mg and Scandium alloy](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/159#issuecomment-6353392941)?
  Is that the specific name for it?
- **[08:10] Sterling:** Scalmalloy.
- **[08:11] Gage:** Scalmalloy? S-C-A-L-A...
- **[08:14] Sterling (?):** I don't think there's an A there. I think it's just Scalmalloy. S-C-A-L-M...
- **[08:22] Student (?):** I'm looking at them.
- **[08:24] Student (?):** Dude, if that thing's going on a pirate ship... like, I don't know where else I could
  find that. [unclear]
- **[08:28]** S-C-A-L-M-A-L-L-O-Y. Scalmalloy. *(several voices)*
- **[08:38] Gage:** Okay, so those are two bases, and...
- **[08:41] Sterling:** For aluminum.
- **[08:42] Gage:** For aluminum. So do both of them use critical minerals in their [composition]? (pass 2:
  "in their protein")
- **[08:47] Sterling:** Only the Scalmalloy.
- **[08:49] Gage:** And so are we trying to discover an alloy that performs better than AlSi10Mg? [08:57] Or uses
  less critical minerals than Scalmalloy?
- **[09:03] Sterling:** The thing is, we have an
  [elemental palette](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/71) that also includes other
  critical minerals that have been used to make aluminum alloys. So Scalmalloy is extremely strong, but it's
  expensive because it has scandium in it (pass 1: "because it has Gage in it"). AlSi10Mg has less of those, but
  it's weaker. And so we can either make something that is just stronger than AlSi10Mg, without dipping into those
  [critical minerals](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/34)...
- **[09:32] Gage:** Yeah.
- **[09:33] Sterling:** And so hopefully we get something that's like, oh, that's stronger than that. That's great.
  That can be a replacement. Or, and/or, we get something that's [as] strong [as] Scalmalloy that's also cheaper
  than Scalmalloy.
- **[09:44] Gage:** Interesting. So overall [it] means in general, not necessarily how many critical elements there
  are?
- **[09:48] Sterling:** Yeah, I mean, the more that there is, that also is expensive.
- **[09:55] Gage:** So the goal is to discover a new alloy that performs better than AlSi10Mg and uses less
  critical minerals than Scalmalloy.
- **[10:01] Sterling:** I'd say "and/or", as we can discover more... Yeah, however you want to say that. Either of
  those options are preferable. If we can do both, even better.
- **[10:15] Gage (?):** [unclear] (pass 1: "Yeah, keeping it as strong as Scalmalloy, and gorgeous"; pass 2: "keep it
  getting stronger and it's got them all away")
- **[10:30] Sterling:** It is unlikely that we [get] above Scalmalloy, but
  [this is the region of interest](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/51).

## 10:36-11:41 Measuring composition: EDS, ICP-MS and silicon

- **[10:36] Ronnie (?):** Just looking at the percentages, I'm not sure how the
  [EDS accuracy](https://github.com/vertical-cloud-lab/caliber/pull/14) is going to be looking. [10:47] So we'll
  probably want to do something... If we can't get the
  [ICP-MS](https://github.com/vertical-cloud-lab/caliber/issues/12#issuecomment-5689310819) or characterization of
  an [alloy with silicon](https://github.com/vertical-cloud-lab/byu-vcl/issues/130#issuecomment-5006966654) figured
  out, we'll probably want to try to do something without silicon, so that we won't have to do an expensive
  process multiple times.
- **[11:04] Gage (?):** I'm guessing we're not just going to find one composition and then be done, right? There
  would be multiple compositions that would be run through before we...
- **[11:14] Sterling:** Oh, we're going to do
  [a ton](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/255), yeah.
- **[11:15] Gage (?):** Okay, yeah.
- **[11:16] Ronnie (?):** So then I'm just wondering, because it looks like they're within like 0.2 to 0.5 weight
  percent, which is still, like... hopefully eventually with EDS, but right now it's not like that.
  [11:29] Unless, um, Timothy finds somewhere that can do our alloys with silicon, you probably want to stay away
  from silicon. There might be other ones that have the same problem. (Both passes have "Timothy".)

## 11:41-14:10 Qualification, independent verification and provenance

- **[11:41] Sterling:** Yeah, and I think this brings another good point up. We will run a bunch of experiments,
  and if we get something in here, and we're going all the way, if we got something here, we would put a lot more
  money into trying to get us closer towards qualification, meaning we would have an independent lab go verify the
  composition (and we have some contacts for that). We would be doing a lot more verification, a lot more
  [independent verification](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/255) for that one,
  where people are going to say, oh, you sent it to this lab and they gave these results; like, we trust those.
  That's all right.
- **[12:48] Sterling:** And then this is another thing, where even if we don't have the composition perfectly
  characterized for every single one, as long as we're doing justice to
  [provenance](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/152#issuecomment-6353388257), we are in
  a good spot to say we can reproduce these results. And if we can reproduce them, then we can figure out some of
  the things that are just a little bit more uncertain. If we get this exact
  [stock powder](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/146) that has these properties, and
  we [atomize it](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/253) with these [settings], and then
  we [sieve it](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/175) in this procedure, and keep
  [the humidity below a certain threshold](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/131)
  throughout the whole process, so [that] we take it to the
  [laser powder bed fusion system](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/138) and run it
  with these parameters under this setting, and then do the
  [tensile test](https://github.com/vertical-cloud-lab/byu-vcl/issues/46) in this way... Like, if we can anchor on
  that, and say with all of those things we get reproducible results, then [comes] our more expensive validation
  stuff, to say yes, the community accepts this as a high-performing alloy, uniquely high quality.
- **[13:58] Gage (?):** I'd actually also like to know: are there already alloys that fall very close to
  [that line](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/51)?
- *[14:09.6: the sound stops for the rest of the 48-minute file]*

---

## References

Everything the speakers refer to, in order.

| Time | What was referred to | Where |
|---|---|---|
| 03:00 | A desktop LPBF printer | [DAL#133](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133) (potential LPBF printer acquisition), [DAL PR 245](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/245) (2026-11-09 desktop LPBF and DED surveys, from the [Nov 9 drop](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6753895964)), [byu-vcl PR 318 comment](https://github.com/vertical-cloud-lab/byu-vcl/pull/318#issuecomment-6613889845) (desktop LPBF systems on the VLM) |
| 03:31 | Putting Carl back on the printer search | [DAL#133 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353364974) (Mar 4: Carl takes it on) and his quotes through [Jul 2](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353367757) |
| 03:31 | A desktop printer at about $50,000 | [DAL#39](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/39) (whether a desktop LPBF machine fits the budget) |
| 04:00-04:35 | Small build plates, baseball-sized volume | [DAL#133 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353368469) (Jul 30 Xact Metal notes: the XMini's 50 mm plate, 65 mm deep), the [LPBF survey's TL;DR](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/153d256/equipment/printer-survey/lpbf-options.md#tldr) |
| 04:00, 12:48 | Tensile tests "in an accepted form" | [byu-vcl#46](https://github.com/vertical-cloud-lab/byu-vcl/issues/46) (ASTM tensile testing standards), [byu-vcl#215](https://github.com/vertical-cloud-lab/byu-vcl/issues/215) (whether a mini tensile tester is enough), [byu-vcl PR 328](https://github.com/vertical-cloud-lab/byu-vcl/pull/328) (tensile bars at three build orientations in the vertical-lab concept) |
| 04:35 | Laser power, heated build plates, hot cracking in Al | [LPBF survey, section 4](https://github.com/vertical-cloud-lab/digital-alloy-lab/blob/153d256/equipment/printer-survey/lpbf-options.md#4-physics-why-al-is-hard-in-lpbf-and-what-is-needed) (why Al is hard in LPBF; plate preheat), [DAL#133 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353368469) (XM200G bed at 100 °C) |
| 04:35 | Printing at the University of Utah | [DAL#138](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/138) (Aconity MIDI through the Spear collaboration), [DAL PR 169](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/169) (setup docs), [DAL PR 232](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/232) (atomizer enclosure parts for the AconityMINI) |
| 05:18 | The 3D Powder Tech contact | [DAL#133 comments](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353365861): Carl emails him (Mar 23), [customizable and open to programmability](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353365995) (Mar 27) |
| 05:18 | He struggled with our powder | [DAL#133 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353366661) (Apr 16: unhappy with the prints, blames the non-spherical powder), [spreadability data](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353366541) (Apr 14) |
| 05:18 | "That powder": the commercial AlSi10Mg powder sent to him | [byu-vcl#8 comment](https://github.com/vertical-cloud-lab/byu-vcl/issues/8#issuecomment-3757060281) (the MSE Supplies AlSi10Mg, 15-45 µm, ordered in January), which Sterling [pointed Carl to](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353366451) as the manufacturer link. Where else the lab has struggled with it isn't said, so it isn't linked |
| 05:44 | The print that came back from him | [DAL#133 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353366838) (Apr 21: Carl posts the photos and data he sent) |
| 06:15 | His printer, in Wisconsin | [DAL#133 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353366142) (Apr 3: powder and plates shipped; the printer is at UW-Madison; [video](https://youtube.com/shorts/9ptU6r6MmJY)) |
| 06:15 | "Like what we did with the [unclear]" | Not identified: the passes heard "PowerGhost airplane" and "power go circle plane" |
| 06:32 | A frugal twin | [byu-vcl#214 comment](https://github.com/vertical-cloud-lab/byu-vcl/issues/214#issuecomment-5670012142) (the lab description: "low-cost, modular benchtop counterparts to expensive instruments"), and the review that named it, [Lo et al., *Digital Discovery* 2024](https://doi.org/10.1039/D3DD00223C) |
| 07:28 | Bigger build plates, a more expensive machine | [DAL#133 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353365218) (Mar 9: ideally 200+ mm build length), [Carl's quotes](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/133#issuecomment-6353367000) (May-Jun) |
| 07:41 | Thermo-Calc | [DAL PR 4](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/4) (Thermo-Calc licensing analysis, HPC examples, AM Module) |
| 07:41 | Getting back to Carl and Xavier on Thermo-Calc and the purchase | [DAL#255](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/255) (first action item) |
| 07:54 | What BYU will charge for the Thermo-Calc licence | [DAL#141](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/141) (Thermo-Calc on the HPC; Xavier, with BYU's research computing) |
| 08:03 | AlSi10Mg and Scalmalloy as the two base alloys | [DAL#255](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/255) (goal), [DAL#159 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/159#issuecomment-6353392941) (start by making known-good AlSi10Mg and Scalmalloy in-house) |
| 09:03 | The elemental palette | [DAL#71](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/71) (bounds for Al and the 15 other elements), [DAL PR 72](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/72), [DAL PR 88](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/88) (shopping list) |
| 09:03 | Critical minerals; scandium in Scalmalloy | [DAL PR 34](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/34) (critical-mineral metrics with Scalmalloy as the comparator), [DAL PR 4](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/4) (Genesis Mission Topic 3B, critical minerals) |
| 10:30, 13:58 | "The region of interest", "that line" (a plot on screen) | Most likely the strength vs critical-mineral trade-off of [DAL PR 51](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/51) (Pareto front of AM Al alloys); the plot itself isn't identified |
| 10:36 | EDS accuracy at 0.2-0.5 wt% | [caliber PR 14](https://github.com/vertical-cloud-lab/caliber/pull/14) (MSA proposal: accurate SEM-EDS of Mg in AlSi10Mg), [byu-vcl PR 95](https://github.com/vertical-cloud-lab/byu-vcl/pull/95) (quantitative EDS) |
| 10:47 | ICP-MS, and alloys with silicon | [caliber#12 comment](https://github.com/vertical-cloud-lab/caliber/issues/12#issuecomment-5689310819) (ICP-MS through Dr. Rappleye's group), [caliber#12 comment](https://github.com/vertical-cloud-lab/caliber/issues/12#issuecomment-5689724636) (Si won't stay in solution without fluoride), [byu-vcl#130 comment](https://github.com/vertical-cloud-lab/byu-vcl/issues/130#issuecomment-5006966654) (Si is awkward for HF-free digestion), [byu-vcl PR 129](https://github.com/vertical-cloud-lab/byu-vcl/pull/129) (HF-free ICP-MS notes), [byu-vcl#110 comment](https://github.com/vertical-cloud-lab/byu-vcl/issues/110#issuecomment-5900790922) (who on campus digests with HF) |
| 11:14 | "A ton" of compositions | [DAL#255](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/255) (40 atomizer runs over three months: 36 aluminum, 4 copper) |
| 11:41 | Independent verification toward qualification | [DAL#255](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/255) ("Take high performers to independent verification") |
| 12:48 | Provenance | [DAL#152 comment](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/152#issuecomment-6353388257) ("as much video and provenance as we can"), [byu-vcl#342](https://github.com/vertical-cloud-lab/byu-vcl/issues/342) (Provenance Eyes: head-worn cameras to record processes, opened by Gage an hour before the meeting) |
| 12:48 | Stock powder with known properties | [DAL#146](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/146) (feedstock purchasing), [DAL#152](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/152) (high-purity Al rod) |
| 12:48 | Atomizing with set parameters | [DAL PR 253](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/253) (atomizer SOP checklist, from [DAL#251](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/251)), [DAL#159](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/159) (repeatability runs) |
| 12:48 | Sieving procedure | [DAL PR 175](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/175) (No. 60 scalp and 20-63 µm LPBF cut), [DAL#234](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/234) (cleaning sieves) |
| 12:48 | Humidity below a threshold | [DAL#131](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/131) (dehumidifiers), [DAL PR 188](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/188) (AirGradient, enclosure vs room humidity) |
| 12:48 | The LPBF system and its parameters | [DAL#138](https://github.com/vertical-cloud-lab/digital-alloy-lab/issues/138) (Utah Aconity), [DAL PR 243](https://github.com/vertical-cloud-lab/digital-alloy-lab/pull/243) (single-track pilot on BYU's Concept Laser M2) |
