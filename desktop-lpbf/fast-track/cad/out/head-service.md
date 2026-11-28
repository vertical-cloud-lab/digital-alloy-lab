# Taking the scan head off on the g3 gantry (`ft_head_service.py`, round 3)

Generated from `ft_model.py` (`P['gantry'] = "four_post_braced_front_g3"`). Beam-tube half-shells, the head's cables and the fibre are off in every route. A route is blocked when a moving part overlaps a fixed one by more than 0.5 mm3 (exact OpenCascade intersection after a python-fcl first pass); 2 mm steps. Parts that touch face to face at the start (MK-09's top flange on the beams, its plate's ends between them, the head on the far-side pad) slide apart without counting.

| State | Route | Result |
|---|---|---|
| FT-1 | A1 MK-09 with the head, lens, input stack and collimator lifted straight up | **blocked at 12.0 mm**: Collimator meets Gantry cross-beam, front (65.3 mm3) |
| FT-1 | A2 the same with the collimator off the mirror block first | free over 160.0 mm |
| FT-1 | B1 head alone (mirror block off) slid +x 46 mm then lifted, far-side plate in place | **blocked at 2.0 mm**: SCANLAB hurrySCAN 25 meets Head far-side support plate, between both cross-beams (33150.0 mm3) |
| FT-1 | B2 the same with the far-side plate and its brackets off first | free over 206.0 mm |
| FT-1 | C  head alone lifted straight up (mirror block and far-side plate off) | **blocked at 2.0 mm**: hurrySCAN input turret meets Scan-head flange plate (418.9 mm3) |
| FT-1V | A1 MK-09 with the head, lens, input stack and collimator lifted straight up | **blocked at 12.0 mm**: Collimator meets Gantry cross-beam, front (65.3 mm3) |
| FT-1V | A2 the same with the collimator off the mirror block first | free over 160.0 mm |
| FT-1V | B1 head alone (mirror block off) slid +x 46 mm then lifted, far-side plate in place | **blocked at 2.0 mm**: SCANLAB hurrySCAN 25 meets Head far-side support plate, between both cross-beams (33150.0 mm3) |
| FT-1V | B2 the same with the far-side plate and its brackets off first | free over 206.0 mm |
| FT-1V | C  head alone lifted straight up (mirror block and far-side plate off) | **blocked at 2.0 mm**: hurrySCAN input turret meets Scan-head flange plate (418.9 mm3) |

Run time 167 s.
