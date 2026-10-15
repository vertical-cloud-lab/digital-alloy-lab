# Edison Result: apex_peer_review

**Task ID:** 46b75f93-d38f-49eb-9262-a3e77c92c9d4

## Findings (2024–2026)

### (a) Is there a peer-reviewed APEX paper by Conn et al.?
No peer-reviewed journal article or conference/proceedings paper describing the **APEX (Autonomous Alloy Prediction and EXperimentation)** system for **DED-based autonomous closed-loop alloy development** by **Conn et al.** (circa 2024–2026) was found in the searches performed here. The only directly matching, authoritative public document retrieved is an **LLNL technical report** hosted by DOE OSTI: **LLNL-TR-2007404** (Conn, S.; Baker, A.), *Self-driving lab to automate the discovery of novel alloys* (June 2025), DOI **10.2172/2584738**. (conn2025selfdrivinglabto pages 1-8)

Most authoritative current reference / URL:
- Conn, S.; Baker, A. (LLNL-TR-2007404, 2025). https://doi.org/10.2172/2584738 (conn2025selfdrivinglabto pages 1-8)

### (b) Has APEX been publicly demonstrated to operate without human monitoring (high hardware autonomy) for structural-metals DED?
The LLNL report contains strong **autonomy goal statements** (e.g., “design, build, and test samples **without human intervention**” and model updating “**without a human in the loop**”). (conn2025selfdrivinglabto pages 1-8, conn2025selfdrivinglabto pages 8-8)

However, in the same report, a photo caption explicitly indicates that during an experimental test run an intern **“monitors the APEX platform.”** This is direct evidence that the publicly documented test run involved human monitoring, and the report does not provide an explicit, verifiable claim of a **fully unmonitored** (lights-out) public DED demonstration for structural metals. (conn2025selfdrivinglabto media 3733be8f, conn2025selfdrivinglabto pages 1-8)

Therefore, based on the available public record retrieved here, **APEX has not been shown (in a citable peer-reviewed or equivalent technical description) to have been publicly demonstrated operating without human monitoring** for structural metals DED.

### (c) How detailed is the implementation in the available report?
The LLNL-TR-2007404 document provides **workflow-level** detail but **not** implementation-level detail:

**What it does describe (high-level):**
- The platform scope: “3D print, grind, polish, and characterize alloy samples.” (conn2025selfdrivinglabto pages 1-8)
- The AM modality: directed-energy deposition (DED) using a high-power laser and powders. (conn2025selfdrivinglabto pages 1-8)
- Characterization/testing modalities named: microscopy, diamond-indentation hardness, and compression testing (“crushing it to assess its response to compression”). (conn2025selfdrivinglabto pages 1-8)
- A sensing/control example: adding a **vibration sensor** to capture operator “feel” during grinding for robotic control. (conn2025selfdrivinglabto pages 1-8)
- Closed-loop concept: collecting data across phases and integrating into a “Materials Acceleration Platform (MAP)” to guide subsequent experiments; aims to update models autonomously. (conn2025selfdrivinglabto pages 8-8)

**What it does not provide (missing/insufficient for reproduction):**
- **Hardware**: no bill of materials; no specific DED machine/laser/nozzle/robot brands or cell architecture; no detailed metrology hardware specs beyond general mentions. (conn2025selfdrivinglabto pages 1-8)
- **Software stack**: no description of orchestration software, robot middleware, data model, experiment scheduler, database/ELN, or error recovery. (conn2025selfdrivinglabto pages 1-8, conn2025selfdrivinglabto pages 8-8)
- **Acquisition function / active learning policy**: MAP is described conceptually, but no explicit optimization formulation (e.g., Bayesian optimization objective, constraints, exploration–exploitation strategy) is documented. (conn2025selfdrivinglabto pages 8-8)
- **Mechanical testing integration**: tests are named, but no integration details are given (sample geometry standards, fixturing/automation, calibration, test conditions, QA/QC, how results feed back to the optimizer). (conn2025selfdrivinglabto pages 1-8)

## Summary table
| Source | Type / status | Peer-reviewed APEX publication (2024–2026)? | Evidence for public operation without human monitoring? | Publicly documented implementation detail level | URL / DOI |
|---|---|---|---|---|---|
| Conn & Baker, **LLNL-TR-2007404** (2025), *Self-driving lab to automate the discovery of novel alloys* | LLNL technical report / OSTI-hosted lab report | **No** — this source is itself a technical report, not a journal or proceedings paper; it describes APEX as the relevant system | **No public proof of unmonitored high-autonomy operation** — report says APEX aims to "design, build, and test samples without human intervention" and to update models "without a human in the loop," but also shows an intern who "monitors the APEX platform during an experimental test run" | **Moderate at workflow level, low at implementation level** — names DED build, grinding/polishing, microscopy, diamond-indentation hardness, compression testing, vibration sensor, MAP closed loop, throughput goal (~48/day); **does not** disclose detailed hardware stack/BOM, software architecture, acquisition function, or detailed mechanical-test integration/protocols | https://doi.org/10.2172/2584738 |
| Peer-reviewed publication search result for APEX (performed searches, 2024–2026 window) | Search outcome | **None found** — no peer-reviewed journal or proceedings paper explicitly describing LLNL APEX for DED closed-loop alloy development was retrieved in the performed searches | **None found** — no peer-reviewed/public source retrieved in these searches documents an unmonitored public demonstration for structural-metals DED | **N/A** — because no peer-reviewed APEX system paper was found, the public implementation detail remains anchored primarily in the technical report above | No authoritative peer-reviewed URL identified in the performed searches |


*Table: This table summarizes the current public evidence on LLNL’s APEX system: whether a peer-reviewed publication exists, whether unmonitored hardware autonomy has been publicly demonstrated, and how detailed the available implementation disclosure is. It is useful for quickly distinguishing the OSTI technical report from the absence of a verified peer-reviewed system paper.*

## Notes on scope/limitations of this verification
This verification is limited to what was retrievable in the tool-accessible scholarly search and full-text evidence above. Within that scope, the record supports that **the commonly cited source is indeed a technical report**, and it does **not** provide sufficient detail to reproduce the full APEX implementation, nor does it document a clearly unmonitored public DED demonstration. (conn2025selfdrivinglabto pages 1-8, conn2025selfdrivinglabto media 3733be8f)