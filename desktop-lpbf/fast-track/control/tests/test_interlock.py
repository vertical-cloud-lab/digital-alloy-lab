"""The hard-wired chain model: no emission with any contact open; every single fault still stops the beam."""
from ftctl import interlock as il


def test_reachability_has_no_path_to_emission_with_a_contact_open():
    r = il.reachability()
    assert r["transitions"] == 4 * (1 << il.N_C) * 16
    assert r["emission_reachable"]
    assert r["emission_with_a_contact_open"] == 0
    assert r["outputs_closed_without_reset"] == 0


def test_single_faults_never_leave_the_beam_on():
    rows = il.single_faults()
    assert all(x["unsafe_demands"] == 0 for x in rows)
    assert all(x["detected_when_operated_alone"] for x in rows)


def test_two_lid_switches_mask_each_other_one_does_not():
    two = {x["fault"]: x for x in il.single_faults()}
    one = {x["fault"]: x for x in il.single_faults([d for d in il.DEVICES if d != "lid_b"])}
    assert not two["stuck_closed:lid_a:ch1"]["detected_by_lid_cycle"]
    assert one["stuck_closed:lid_a:ch1"]["detected_by_lid_cycle"]
    # welded safety-relay outputs are caught by the laser's own channel monitoring
    assert two["welded:G9SE output 13-14"]["masked_by_n"] == 0
