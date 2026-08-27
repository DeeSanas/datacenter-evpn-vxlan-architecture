# EVPN Control-Plane Reference

This note describes concepts rather than vendor CLI.

## Key EVPN route types

### Type 2 — MAC/IP Advertisement

Used to advertise endpoint MAC addresses and, when available, their associated IP addresses. This replaces flood-and-learn behavior for much of the endpoint reachability information distributed between VTEPs.

### Type 3 — Inclusive Multicast Ethernet Tag

Supports discovery of VTEPs participating in a broadcast domain and handling of BUM traffic according to the chosen replication model.

### Type 5 — IP Prefix Route

Used for advertising IP prefixes in EVPN designs that provide routed tenant reachability. Exact support and implementation behavior must be validated for the selected platform.

## Route distinguisher

The RD makes otherwise identical routes unique in BGP. It is not itself the import/export policy.

## Route target

RTs determine which VPN/EVPN routes are imported into or exported from a tenant context. Use an allocation convention that is predictable and automatable.

## L2 VNI

Represents a tenant Layer-2 segment/broadcast domain across VTEPs. Example:

```text
VLAN 110 -> VNI 10110
VLAN 120 -> VNI 10120
```

## L3 VNI

Represents a routed tenant/VRF context. Multiple L2 VNIs may participate in one tenant VRF and use a common L3 VNI for routed connectivity depending on platform design.

## Anycast gateway

A distributed anycast gateway allows endpoints on different leaves to use a consistent default-gateway identity while routing can occur close to the endpoint. MAC/IP conventions and synchronization behavior are platform-specific and must be tested.

## Control-plane validation

For each tenant/segment verify:

- expected VTEPs advertise/receive the intended routes;
- RT import/export matches the segmentation policy;
- MAC/IP mobility is handled as expected;
- stale routes clear after endpoint or leaf failure;
- external Type-5 or IP routing is filtered correctly;
- no unintended tenant route leakage occurs.
