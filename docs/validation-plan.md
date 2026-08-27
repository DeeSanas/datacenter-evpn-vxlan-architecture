# Fabric Validation Plan

## Baseline underlay

| Test | Expected result |
|---|---|
| Leaf-to-spine adjacencies | All intended sessions/neighbors established |
| Loopback reachability | Every VTEP loopback reachable through redundant paths |
| ECMP | Multiple equal-cost next hops visible where designed |
| MTU | Encapsulated payload passes end to end without fragmentation issue |
| Route filtering | Only intended infrastructure prefixes exchanged |

## Overlay

Validate:

- EVPN sessions established;
- expected L2/L3 VNIs operational;
- local endpoint MAC/IP learned correctly;
- remote endpoint routes received from expected VTEP;
- same-subnet traffic crosses VXLAN overlay;
- inter-subnet traffic uses the intended distributed gateway/VRF;
- tenant A cannot reach tenant B unless policy explicitly permits it;
- north-south advertisements contain only approved prefixes.

## Failure scenarios

### Single leaf-spine link loss

Expected: affected traffic reconverges to remaining ECMP path without loss of unrelated tenant reachability.

### Single spine loss

Expected: leaves retain reachability through remaining spine(s); control-plane sessions and data-plane paths converge within the documented target.

### Border-path loss

Expected: external routes withdraw or change preference predictably without leaking unintended paths.

### Leaf/VTEP loss

Expected: routes sourced only by the failed VTEP are withdrawn; dual-attached services follow the selected multihoming design if implemented.

## Evidence to capture

For a portfolio lab or production acceptance test, retain:

1. topology/version inventory;
2. route/neighbor state before test;
3. timestamped failure action;
4. packet-loss/convergence observation;
5. route/neighbor state after convergence;
6. application reachability result;
7. telemetry/alert evidence;
8. rollback/recovery confirmation.

The purpose is to demonstrate measurable behavior rather than simply stating that redundancy exists.
