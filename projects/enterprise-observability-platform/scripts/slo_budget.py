#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail("usage: slo_budget.py <slo.json>")

    data = json.loads(Path(sys.argv[1]).read_text())
    required = ["window_days", "availability_target", "total_requests", "bad_requests"]
    for key in required:
        if key not in data:
            fail(f"missing field: {key}")

    days = float(data["window_days"])
    target = float(data["availability_target"])
    total = int(data["total_requests"])
    bad = int(data["bad_requests"])

    if days <= 0:
        fail("window_days must be positive")
    if not 0 < target < 1:
        fail("availability_target must be between 0 and 1")
    if total <= 0 or bad < 0 or bad > total:
        fail("request counts are invalid")

    total_minutes = days * 24 * 60
    allowed_unavailable_minutes = total_minutes * (1 - target)
    allowed_bad_requests = total * (1 - target)
    observed_good_fraction = (total - bad) / total
    consumed_fraction = bad / allowed_bad_requests if allowed_bad_requests else 0

    print(f"Service: {data.get('service', 'unnamed')}")
    print(f"SLO target: {target * 100:.3f}% over {days:g} days")
    print(f"Time-based error budget: {allowed_unavailable_minutes:.2f} minutes")
    print(f"Request-based error budget: {allowed_bad_requests:.0f} bad requests")
    print(f"Observed good-request percentage: {observed_good_fraction * 100:.4f}%")
    print(f"Error budget consumed: {consumed_fraction * 100:.2f}%")

    if bad > allowed_bad_requests:
        print("SLO status: BREACHED")
    else:
        print("SLO status: WITHIN BUDGET")


if __name__ == "__main__":
    main()
