Genesis-Mission-RFA-FAQs-20260410-v2.pdf
PDF
DE-FOA-0003612-000003.pdf
PDF
Aside: here are the official docs, which I'll ask you to reference sometimes
Summer salary is good. Keep that fixed.
3 MS students is good, but fix the total
Spelling should be Valimet

Travel for each of the 3 MS students + PI to one conference (TMS / MS&T / MRS)
The six validation trips would be taken by students, not by PI (noting that not every collaborator would necessitate BYU personnel being there)
Put three 3-day trips to Stockton, CA for Valimet (two people), consistent with doing three rounds of 2 unique compositions

Assume $3-$10 / lb for ingot material (i.e., the entirety of the gas-atomization material cost, likely from Bellmont Technologies (sp?), Eutectix (sp?), and AMG something or other), and 500 lbs per material, with a total of 6 materials (distinct ingot compositions), 6 because it's three rounds of two

And yes, let's pull out from the word doc and work in a canvas together
Can you keep formatting? Or would you need a word doc for that?
Let's go with markdown for now that will be converted to word
Revised Budget Justification (working Draft)
Give the range, and put $25k for budgeting purposes
Revised Budget Justification (working Draft)
How much would 5N inert gas cost?
Revised Budget Justification (working Draft)
put in parantheses what the LPBF consumables are
Revised Budget Justification (working Draft)
flaime-genesis-proposal-clean (6).pdf
PDF
There also needs to be a pretty big budget line item dedicated to the distributed validation network (see attached proposal, in draft state, and ignore the budget numbers - just trying to convey what the validation network is, and assume on average $2k/collaborator that's committed, some will be free - others will require user facility fees, etc.)
Revised Budget Justification (working Draft)
Did you see how many collaborators were listed?
Revised Budget Justification (working Draft)
How many letters were there in there?
Revised Budget Justification (working Draft)
I made some updates
Revised Budget Justification (working Draft)
Account for 2x cost and state 5N Ar
Revised Budget Justification (working Draft)
The research scale elemental feedstock needs to be justified. Did this get lost from the original document? I thought it had way more detail
Revised Budget Justification (working Draft)
Are there other details like that that got lost from the original document?
Yes
Revised Budget Justification (working Draft)
Let's estimate the research-scale feedstock costs a bit more. We already pinned down pounds and price per lb for ingots for gas atomization. For research scale, it depends on how much we atomize in a given run. For context, the induction crucible size is 225 cm^3, and we will assume prints are on the Mastrex MX-120 (120 mm diameter, assuming samples lay flat, and assume that the hopper has to be filled to 3x the volume of the print, and make an estimate for the density of the powders:

For example, AlSi10Mg powder likely has a tap density around 1.6 g/cm^3 and an apparent density around 1.3 g/cm^3 (would need to be verified). In solid, dense form, closer to 2.6g/cm3
Revised Budget Justification (working Draft)
Point out the in-house BYU Mastrex MX-120 (in-kind from BYU) and the UofU Aconity MIDI (Build size is 170mm diameter x 200 mm build height), same assumption about part height and hopper needing to be filled to 3x the build height
Try again, also remove the line about "prior spot purchasing"?
Start a new canvas I guess since you're having trouble editing the old one: # Budget Justification

**Brigham Young University**

## A. Senior/Key Personnel

BYU faculty salary is calculated off an 8-month academic base. This support is valuable in providing resources for dedicated faculty support during the productive summer months.

**PI: Dr. Sterling Baird** — Faculty summer support is requested [per-person salary detail removed].

**Fringe Benefits:** The 2026 fringe benefit rate for faculty summer salary is 19.7%. [Per-person fringe detail removed.]

## B. Other Personnel

**Graduate Student Research Assistant:** Three full-time (28 hours a week) graduate students will work throughout the 9 months of this project. The MS students will lead BOFN software integration / data pipeline and experimental data ingest / CALPHAD automation under PI supervision. [Per-person rate detail removed.]

**Undergraduate Student Research Assistants:** 12 undergraduate students will be hired hourly to work on this project. Students are staggered across pipeline roles (atomization, LPBF handoff, SEM/EDS characterization, tensile, data engineering) with intentional redundancy so each role has continuous coverage across terms. Rates reflect BYU’s published undergraduate research pay scales for laboratory work involving powder handling and certified instrumentation. [Per-person rate detail removed.]

**Fringe Benefits:** No fringe rate applies to student salaries during periods when students are enrolled in classes. No fringe benefits are requested for students.

## D. Travel

**Validation:** Six trips are requested to various collaborators to validate the printing. These trips will be taken by students rather than by the PI, noting that not every collaborator interaction will require BYU personnel on site.

**Valimet Coordination:** Three 3-day trips to Stockton, California are requested for coordination with Valimet. Each trip will include two BYU personnel and is aligned with three rounds of processing for two unique compositions.

**DOE Genesis Program Meeting:** One trip is requested for the PI to attend the annual DOE Genesis Program Meeting.

**Conference:** Travel is requested for each of the three MS students and the PI to attend one technical conference (TMS, MS&T, or MRS) to disseminate the results of the research.

Travel budget is requested for **$1,500 per trip (17 traveler-trips total). Total requested is $25,500.**

### Details Per Trip

* Airfare: $600
* Meals (per diem: $74/day × 4 days): $296
* Lodging ($133 × 3 nights): $399
* Ground Transportation: $205

**Travel Total per Trip: $1,500**

## F. Other Direct Costs

### Materials and Supplies

* **Research-scale elemental feedstock:** $36,000
  (sized from powder throughput and build geometry across both in-house and partner LPBF systems. At BYU, builds are performed on the in-kind **Mastrex MX-120** (120 mm diameter). At UofU, builds are performed on the **Aconity MIDI** (170 mm diameter × 200 mm height). Assuming ~5 mm effective part height and 3× hopper fill:

  * MX-120: area ≈113 cm² → part volume ≈56 cm³ → powder ≈170 cm³ → ≈220 g/build (1.3 g/cm³ apparent density)
  * Aconity MIDI: area ≈227 cm² → part volume ≈113 cm³ → powder ≈340 cm³ → ≈440 g/build

  Using a blended estimate (~300 g/build) over ~320 builds yields ≈96 kg powder demand; applying ~2× factor for losses, recycling inefficiency, and failed prints gives ≈190 kg total material demand. Elemental feedstock is purchased at research-grade purity (99.9%+) and blended per composition, with effective costs dominated by minor additions (Sc, Er, etc.) even at trace levels. Assuming blended effective costs on the order of ~$150–$200/kg yields ~$14k–$38k baseline, with contingency and lot-size effects supporting the $36,000 request.)

* **Gas-atomization feedstock (Valimet ingot material):** $25,000
  (6 distinct ingot compositions × 500 lb each = 3,000 lb total; $3–$10/lb range corresponds to $9,000–$30,000 total; $25,000 used for budgeting purposes)

* **Inert gas (5N-grade Ar, Ar-rich feed):** $20,000
  (assumes ~2× cost relative to 4.5N-grade argon due to higher purity requirements)

* **High-purity machined Al crucibles:** $3,000

* **Sonotrode tip replacement contingency:** $2,500

* **LPBF consumables:** $4,000 (build plates, recoater blades, shielding gas filters, powder handling/transfer consumables, sieves, and minor maintenance items)

* **UofU Metal 3D Printing Core Facility recharge:** $12,000

* **Metallographic supplies:** $3,000

* **Characterization facility recharge fees:** $27,000

* **ASTM E8/E8M tensile grips/fixtures and ISO 52902 artifact preparation:** $3,000

* **Safety / PPE:** $5,968

* **Distributed validation network (multi-site LPBF/DED/Binder jet metal 3D printing partner validation, see appendix 7):** $40,000
  (≈20 collaborators at ~$2,000 per committed site on average; some sites contribute in-kind while others require user facility fees)

**Total Supplies: TBD**

### Research Publication Costs

Open-access publication fees for 2 Phase I papers. **Total requested is $3,000.**

### Contract Services

* AmSC hosting and artifact exchange: $1,500
* Lab-safety and powder-handling training certifications: $1,500
* Hazmat waste disposal and Ar cylinder rental: $900

**Total requested is $3,900.**

### Graduate Student Tuition

Tuition is budgeted for all graduate students. Full tuition for Fall 2026 and ¾ tuition for Winter 2027 semesters is $7,588 per student. For 3 graduate students, **total requested is $22,764.**

## G. Total Direct Costs

**TBD**

## H. Indirect Costs

BYU’s DHHS federally negotiated indirect cost rate is 51.5% based on modified total direct costs (MTDC).

* MTDC Base: TBD
* F&A Rate: 51.5%
* Total Indirect Costs: TBD

## I. Total Amount Requested

**TBD**

Asked ChatGPT

Budget Justification (markdown Working Copy V2)
also the experimental design
Budget Justification (markdown Working Copy V2)
Assume $20/hr for undergrad wages
Budget Justification (markdown Working Copy V2)
What about the high-purity Al crucibles? We will machine these in-house for negligible cost, but what is the purity and is the cost estimate reasonable? Assume an average of 50-70% of the total material weight being due to this high-purity aluminum bar feedstock, and adding in Al shot to fill the balance of Al where needed
Budget Justification (markdown Working Copy V2)
This needs to line up with text in feedstock paragraph, i.e., both need to mention each other
Budget Justification (markdown Working Copy V2)
I made an update
Budget Justification (markdown Working Copy V2)
What's better, assume tap density maybe?
Budget Justification (markdown Working Copy V2)
Sure add the parantheses
Budget Justification (markdown Working Copy V2)
Are the characterization fees good? Do you need an hourly cost?
Budget Justification (markdown Working Copy V2)
mention the $30/hr BYU rate
Budget Justification (markdown Working Copy V2)
Does AAmSC hosting and artifact exchange need to be in there? That seems random
Budget Justification (markdown Working Copy V2)
Is contract services the right top-level category for lab safety and hazmat?
Budget Justification (markdown Working Copy V2)
Update the total since i removed the amsc line
Budget Justification (markdown Working Copy V2)
Add two BYU capstone projects ($22k/team)
Budget Justification (markdown Working Copy V2)
For context, here are the two teams, and noting that it was clarified to me F&A doesn't apply to capstone teams:

Team A — Lab Operations Toolkit (mechanical / manufacturing focus). Our lab takes raw metal feedstock, melts and sprays it into a fine metal powder, and then 3D-prints test parts from that powder; this team would design the operator-facing fixtures, checklists, and simple data-logging tools that make the powder-making step safe, repeatable, and easy to hand off to the next station. Deliverables would include physical fixtures, written standard operating procedures, and a lightweight digital "job traveler" that records who did what and when. Disciplines: mechanical and manufacturing engineering, with optional electrical or computer-science support; ~5–6 students.

Team B — Research Data & Sample-Tracking System (software / systems focus). Across the project, every batch of powder, every printed part, and every test result needs to be linked together so we can later ask, "where did this part come from and how did it perform?" — this team would build the internal web-based intake forms, sample-ID/tracking workflow, and dashboard that tie those records into a single source of truth for the lab. Deliverables would include a working web application, a structured data schema, and import/export tools so results can be shared with our university and industry partners. Disciplines: computer science and software/IT, with manufacturing or mechanical engineering for domain context; ~5–7 students.
Budget Justification (markdown Working Copy V2)
Recompute
Budget Justification (markdown Working Copy V2)
[BYU/Valimet budget split removed from the public copy]
Budget Justification (markdown Working Copy V2)
Assume $1k on average for validation network (confirmed through email exchanges)
Budget Justification (markdown Working Copy V2)
Ok, what's next
Budget Justification (markdown Working Copy V2)
[BYU/Valimet budget split removed from the public copy]
Budget Justification (markdown Working Copy V2)
Start a new canvas, copy over what you have, so you can make new edits
Budget Justification (working Copy V3)
$1500/trip might be a bit high, not sure. Valimet is in CA, assume all the other trips are domestic (though probably a lot on east coast)
Budget Justification (working Copy V3)
Compute exact BYU direct
Solve MTDC + F&A precisely
Budget Justification (working Copy V3)
Remove 4 undergrads, since undergrads will significantly boost required hours
Budget Justification (working Copy V3)
Remove 1 MS student
Budget Justification (working Copy V3)
Create a new canvas and edit
Budget Justification (working Copy V4 - Optimized)
What happened to the details for materials and supplies?
Budget Justification (working Copy V4 - Optimized)
You also lost details for other sections like grad student tuition
Budget Justification (working Copy V4 - Optimized)
Lost details on research publication, maybe elsewhere. Look at the original
Budget Justification (working Copy V4 - Optimized)
You lost the specifics around the two capstone teams
Budget Justification (working Copy V4 - Optimized)
It's supposed to be 2 capstone teams