# Design Principles

## 1. Keep the physical fabric routed

Use point-to-point Layer-3 links between leaves and spines. Tenant bridging belongs in the overlay; do not extend application VLANs through the physical spine layer without a specific, reviewed reason.

## 2. Make every leaf path equivalent where practical

A leaf should normally connect to every spine so the underlay can use ECMP and tolerate individual spine/link loss without topology redesign.

## 3. Separate identity, transport and tenant policy

- loopbacks identify network nodes/VTEPs;
- the underlay transports packets between VTEPs;
- EVPN carries tenant reachability;
- VRFs/VNIs define tenant segmentation.

This separation makes troubleshooting easier than combining all roles into one addressing and routing domain.

## 4. Engineer MTU, do not assume it

VXLAN adds encapsulation overhead. Select an underlay MTU with sufficient headroom and validate host-to-host effective MTU. Mixed MTU is a common cause of intermittent application behavior.

## 5. Route targets are policy

Route-target import/export controls which EVPN routes enter a tenant VRF. Treat RT design as segmentation policy, document it, and avoid accidental broad import patterns.

## 6. Border connectivity must have explicit route ownership

Define where default routes, enterprise prefixes and tenant routes are learned/advertised. Apply filtering at external boundaries and document route preference to avoid unintended transit behavior.

## 7. Keep management recoverable when the fabric is unhealthy

Use an independent OOB management plane for console/BMC/network-management access where operational requirements justify it. The recovery path should not depend entirely on the network being recovered.

## 8. Automate from an intent model

A structured data model should describe nodes, interfaces, ASNs, loopbacks, VNIs and VRFs. Vendor templates can then be generated from the same intent rather than maintaining unrelated hand-built configurations.

## 9. Failure convergence is a requirement

Measure what happens when links, spines, border paths and leaf nodes fail. Redundancy on a diagram has little value without deterministic convergence and observable failure behavior.
