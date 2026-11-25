# Layer light: what each LED position shows (`analysis/optics/layer_light.py`)

Camera: pupil at (98, -59, 178), 32.7° off vertical, from the front-right (azimuth -31° from +x); 12 mm lens, 26 µm per pixel. Streaks from a nicked blade run along x (the recoat direction), so light needs a y component to shadow them. 'Across streaks' is the mean |sin| of the light's azimuth against x (1 = straight across). Shadow = what a 100 µm step casts; 'visible' subtracts the part the step hides from the camera. 'Mirror to camera' is the smallest angle between the plate's mirror reflection of the light and the camera: well above ~10° means fused metal shows dark and powder bright (dark field); near 0 it glares. 'Glint tilt' is the facet slope that reflects the light into the camera. 'Uniformity' is the brightest over the dimmest lit point (Lambertian emitter, 1/d²). 'Reached' is the share of the plate that sees more than half of the source past the dose chute, the blade at park, the gas knife and the recoater screw.

| Light | Plate | Elevation (°) | Across streaks | Shadow of 100 µm (px) | Visible to the camera (px) | Mirror to camera (°) | Glint tilt (°) | Uniformity | Reached (%) |
|---|---|---|---|---|---|---|---|---|---|
| A. inside, low on the right wall (round 4) | S25 | 13–16 | 0.04 | 13.7–16.6 | 11.9–14.2 | 100 | 51–55 | – (blocked) | 0 |
| A. inside, low on the right wall (round 4) | M50 | 12–17 | 0.08 | 12.3–18.0 | 10.7–15.4 | 95 | 49–57 | – (blocked) | 0 |
| A. inside, low on the right wall (round 4) | L75 | 11–20 | 0.12 | 10.8–19.5 | 9.6–16.5 | 89 | 46–59 | – (blocked) | 0 |
| B. inside, lid underside (as drawn) | S25 | 38–44 | 0.04 | 4.0–4.9 | 2.1–2.5 | 73 | 37–43 | 1.4 | 100 |
| B. inside, lid underside (as drawn) | M50 | 36–47 | 0.08 | 3.6–5.3 | 1.9–2.7 | 66 | 34–45 | 1.9 | 100 |
| B. inside, lid underside (as drawn) | L75 | 34–51 | 0.12 | 3.2–5.8 | 1.7–2.9 | 60 | 30–47 | 2.6 | 100 |
| C. inside, low on the back wall | S25 | 12–16 | 1.00 | 13.3–17.8 | 13.3–17.8 | 55 | 33–42 | 2.1 | 100 |
| C. inside, low on the back wall | M50 | 11–19 | 0.99 | 11.1–20.0 | 11.1–20.0 | 48 | 28–46 | 4.4 | 100 |
| C. inside, low on the back wall | L75 | 10–23 | 0.98 | 8.9–22.2 | 8.9–22.2 | 40 | 23–50 | 9.5 | 100 |
| D. outside, new low window in the back wall, left of the inlet plenum | S25 | 9–11 | 0.67 | 20.0–23.6 | 20.0–23.6 | 44 | 22–28 | 1.6 | 100 |
| D. outside, new low window in the back wall, left of the inlet plenum | M50 | 9–12 | 0.67 | 18.2–25.4 | 18.2–25.4 | 41 | 20–31 | 2.6 | 100 |
| D. outside, new low window in the back wall, left of the inlet plenum | L75 | 8–13 | 0.66 | 16.4–27.2 | 16.4–27.2 | 37 | 19–35 | 4.3 | 100 |
| E. outside, new low window in the back wall, right of the inlet plenum | S25 | 9–11 | 0.67 | 20.0–23.6 | 19.5–22.6 | 86 | 48–53 | 1.6 | 100 |
| E. outside, new low window in the back wall, right of the inlet plenum | M50 | 9–12 | 0.67 | 18.2–25.4 | 17.9–24.2 | 80 | 45–56 | 2.6 | 100 |
| E. outside, new low window in the back wall, right of the inlet plenum | L75 | 8–13 | 0.66 | 16.4–27.2 | 16.4–25.8 | 75 | 42–58 | 4.3 | 100 |
| F. outside, new low window in the right wall | S25 | 9–11 | 0.07 | 19.6–23.5 | 17.9–21.2 | 103 | 53–57 | – (blocked) | 0 |
| F. outside, new low window in the right wall | M50 | 9–12 | 0.09 | 17.7–25.5 | 16.2–22.9 | 98 | 51–59 | – (blocked) | 0 |
| F. outside, new low window in the right wall | L75 | 8–14 | 0.12 | 15.8–27.4 | 14.6–24.6 | 93 | 48–60 | – (blocked) | 0 |
| G. outside, through the camera's own window (beamsplitter) | S25 | 55–60 | 0.51 | 2.2–2.7 | 0.0–0.0 | 60 | 30–35 | 1.2 | 100 |
| G. outside, through the camera's own window (beamsplitter) | M50 | 52–63 | 0.51 | 1.9–3.0 | 0.0–0.0 | 54 | 27–38 | 1.4 | 100 |
| G. outside, through the camera's own window (beamsplitter) | L75 | 50–66 | 0.51 | 1.7–3.3 | 0.0–0.0 | 47 | 24–40 | 1.7 | 100 |

Main laser window: 12 of 108 rays from a light ring between the window's retaining ring and the f-theta (r 23–45 mm, z 165–185) reach the L75 plate through the Ø44 ring and the Ø42 bore: only from r = 23, 30 mm, onto x -38 to 10 mm of the plate, at 70–86° elevation. A light there sits against the beam's own envelope (the L75 edge ray passes r ≈ 19–26 mm at that height for k 0.33–0.63) and in the scattered 1070 nm light, and it lights only the far side. The window's aperture is the beam's, so it can't carry the light.

Light positions: A. inside, low on the right wall (round 4): LED bar on the +x wall, z 30-38 (trapped the right liner); B. inside, lid underside (as drawn): LED bar x 126-134, z 112-120, along y (cad/lpbf_low.py section 7); C. inside, low on the back wall: LED bar on the back wall under the ball screw, in front of the lower back liner; D. outside, new low window in the back wall, left of the inlet plenum: Ø20 clear window at x -105, z 25 (the plenum's flange covers x ±78, z < 40 outside; a KF40 flange there clears it); LED behind it; E. outside, new low window in the back wall, right of the inlet plenum: Ø20 clear window at x +105, z 25; F. outside, new low window in the right wall: Ø20 clear window at y +10, z 25, under the vacuum-port adapter (z 42-98); G. outside, through the camera's own window (beamsplitter): coaxial with the camera; the Ø20 aperture only passes light from on the camera's axis.
