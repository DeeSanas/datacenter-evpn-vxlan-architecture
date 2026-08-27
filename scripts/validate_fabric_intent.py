#!/usr/bin/env python3
"""Validate the reference EVPN-VXLAN fabric intent model.

This validator checks structural and allocation rules that are useful in a lab
or CI pipeline. It does not replace vendor configuration validation.
"""

from __future__ import annotations

import ipaddress
import sys
from pathlib import Path

import yaml


def fail(message: str) -> None:
    raise ValueError(message)


def validate(path: Path) -> None:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail("Top-level YAML object must be a mapping.")

    fabric = data.get("fabric") or {}
    if fabric.get("overlay", {}).get("protocol") != "bgp-evpn":
        fail("fabric.overlay.protocol must be bgp-evpn")
    if fabric.get("overlay", {}).get("encapsulation") != "vxlan":
        fail("fabric.overlay.encapsulation must be vxlan")

    nodes = data.get("nodes") or {}
    all_nodes = list(nodes.get("spines") or []) + list(nodes.get("leaves") or [])
    if not all_nodes:
        fail("At least one node must be defined.")

    names: set[str] = set()
    loopbacks: set[str] = set()
    vteps: set[str] = set()

    for node in all_nodes:
        name = node.get("name")
        if not name or name in names:
            fail(f"Node name missing or duplicated: {name!r}")
        names.add(name)

        loopback = node.get("loopback")
        if not loopback:
            fail(f"Node {name} is missing loopback")
        ipaddress.ip_interface(loopback)
        if loopback in loopbacks:
            fail(f"Duplicate loopback: {loopback}")
        loopbacks.add(loopback)

        if "vtep" in node:
            vtep = node["vtep"]
            ipaddress.ip_interface(vtep)
            if vtep in vteps:
                fail(f"Duplicate VTEP: {vtep}")
            vteps.add(vtep)

    tenants = data.get("tenants") or []
    l2_vnis: set[int] = set()
    l3_vnis: set[int] = set()
    vlans: set[int] = set()

    for tenant in tenants:
        tenant_name = tenant.get("name", "<unnamed>")
        l3_vni = int(tenant.get("l3_vni", 0))
        if l3_vni <= 0 or l3_vni in l3_vnis:
            fail(f"Invalid or duplicate L3 VNI for {tenant_name}: {l3_vni}")
        l3_vnis.add(l3_vni)

        for segment in tenant.get("segments") or []:
            vlan = int(segment.get("vlan", 0))
            l2_vni = int(segment.get("l2_vni", 0))
            gateway = segment.get("gateway")

            if not 1 <= vlan <= 4094 or vlan in vlans:
                fail(f"Invalid or duplicate VLAN: {vlan}")
            if l2_vni <= 0 or l2_vni in l2_vnis:
                fail(f"Invalid or duplicate L2 VNI: {l2_vni}")
            if not gateway:
                fail(f"Segment in {tenant_name} is missing gateway")

            ipaddress.ip_interface(gateway)
            vlans.add(vlan)
            l2_vnis.add(l2_vni)

    print("Fabric intent validation passed")
    print(f"Nodes: {len(all_nodes)}")
    print(f"Tenants: {len(tenants)}")
    print(f"L2 VNIs: {len(l2_vnis)}")
    print(f"L3 VNIs: {len(l3_vnis)}")


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "models/fabric-intent.yaml")
    try:
        validate(path)
    except (OSError, ValueError, TypeError, yaml.YAMLError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
