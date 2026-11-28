# `microbalance`: Sartorius Cubis II MCA6.6S-2S00-M micro balance (SOP 01, #262)

SOP 01 weighs 10–25 mg of powder into an 85 µL alumina crucible, so the balance needs microgram readability and a
small glass draft shield. The model is the Sartorius Cubis II MCA6.6S-2S00-M (6.1 g × 1 µg). It was chosen over the
Mettler Toledo XPR micro balances because Sartorius publishes the dimensions of each module and has a video of the
balance in use. mt.com refused the research requests, so the XPR's dimensions came only from unverified search
snippets.

## Sources

| What | Source |
|---|---|
| Weighing module 340 × 139 × 129 mm (L × W × H); electronics module 355 × 260 × 61 mm; pan ø 30 mm; 6.1 g × 0.001 mg | Sartorius Cubis II data sheet, p. 3 ([PDF, Thermo Fisher copy](https://assets.thermofisher.com/TFS-Assets/ANZ/brochures/sartorius-cubis-ii-datasheet.pdf)) |
| "Automatic, motorized, round 100 % glass" draft shield | same, p. 15 |
| Chamber height 70 mm; 7 in touch display | Rice Lake catalogue page, Cubis II MCA micro ([PDF](https://www.ricelake.com/media/elopujy1/2026_cubisii_mca_micro.pdf)) |
| Look: a long white module, full height behind the chamber and stepped down at the back; the round glass chamber on a white pedestal at its front end; a blue strip beside it; the flat electronics module with the tilted display | Sartorius, "Overview of the Cubis II Microbalance", [youtu.be/7EjFumYx1eo](https://youtu.be/7EjFumYx1eo) at 1:44–1:52 |

## Published and model dimensions

| | Published | Model |
|---|---|---|
| Weighing module L × W × H | 340 × 139 × 129 mm | 340 × 139 × 129 mm (pedestal included in the 340) |
| Electronics module | 355 × 260 × 61 mm | 355 × 260 × 61 mm |
| Pan | ø 30 mm | ø 30 mm, 36 mm over the bench (estimate) |
| Chamber height | 70 mm | 70.9 mm (fitted) |
| Chamber diameter | – | 88.3 mm (fitted) |
| Back part's height, the step | – | 103.9 mm, 165 mm behind the module's front face (fitted) |

## Registration (`fit.py solve microbalance`)

| View | Frame | Picks | RMS, starting model | RMS, fitted | Lens |
|---|---|---|---|---|---|
| `sartorius_109` | Sartorius video 1:49 | 6 points (back corners, the step, the blue strip) and 3 on the chamber's top rim | 3.87 px | 1.73 px | 1061 px (62°) |

There is **no held-out view**. Every shot in Sartorius's video that shows the module whole comes from one fixed camera
(1:44, 1:46, 1:49 and 1:51 are the same framing), and the close-ups show only the display. The module's front corners
are hidden behind the chamber glass and the pedestal, so they are not picked. The electronics module is hidden in the
overlay (`"pose": {"electronics": 0}`): the bench layout puts it to the right of the weighing module, where the
operator's tools leave room, not in front of it as in the video.

## What is uncertain

- **How the draft shield opens.** Sartorius says "motorized, round"; the model turns a 120° glass segment 130° round
  the chamber to open its front. The real mechanism (a rotating cylinder with an opening, or segments) is not shown
  close up in the video.
- **The pan's height** in the chamber is an estimate.
- The display's angle and the module's fillets are from the frames, not measured.
