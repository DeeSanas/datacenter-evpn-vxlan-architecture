# Enterprise Observability Platform Reference Architecture

A vendor-neutral observability reference architecture for enterprise infrastructure, Kubernetes, cloud and application environments. The design separates telemetry collection, transport, storage, correlation and consumption so metrics, logs, traces and events can support both operations and service-level management.

> **Positioning:** This is a reference architecture and SRE lab. It is not presented as a customer production deployment, and the example SLOs are engineering examples rather than service commitments.

## Design goals

- Standardize collection of metrics, logs, traces, audit events and infrastructure telemetry
- Decouple telemetry producers from storage and visualization backends
- Preserve service context through consistent labels and resource attributes
- Support centralized alerting while avoiding one monolithic failure domain
- Define SLI/SLO/error-budget calculations that can be reproduced from data
- Retain telemetry according to value, regulatory needs and cost
- Protect observability platforms from becoming unrestricted paths into production systems

## Logical architecture

See [`diagrams/observability.mmd`](diagrams/observability.mmd).

```text
Applications / Kubernetes / Cloud / Network / Storage
                       |
      Agents / Exporters / OpenTelemetry Collectors
                       |
           Processing / Enrichment / Routing
             |           |           |
           Metrics      Logs       Traces
             |           |           |
             +------ Telemetry Stores ------+
                            |
                 Dashboards / Alerting
                            |
              SRE / NOC / SOC / Engineering
```

## Telemetry model

| Signal | Primary use |
|---|---|
| Metrics | Capacity, saturation, rates, health, SLI calculations |
| Logs | Event detail, audit, diagnostics, security investigation |
| Traces | Request-path latency and distributed dependency analysis |
| Events | Deployment, configuration, incident and lifecycle context |
| Network telemetry | Reachability, path health, utilization and flow behavior |

## SRE principles represented

- Alerts should be actionable and tied to user/service impact where possible.
- Dashboards should expose service health, not only component health.
- SLOs require explicitly defined SLIs, measurement windows and exclusions.
- Error budgets turn reliability targets into a measurable engineering constraint.
- Telemetry retention should match operational value rather than keeping all data indefinitely.

## Included artifacts

- [`diagrams/observability.mmd`](diagrams/observability.mmd) — editable architecture diagram
- [`models/slo.json`](models/slo.json) — example service-level objective model
- [`scripts/slo_budget.py`](scripts/slo_budget.py) — SLO/error-budget calculator

## SLO calculation

```bash
python projects/enterprise-observability-platform/scripts/slo_budget.py \
  projects/enterprise-observability-platform/models/slo.json
```

The example demonstrates both time-based availability budget and request-based error-budget consumption.

## Architecture decisions to make in production

- Which telemetry signals must remain local and which may be centralized?
- What collection failure behavior is acceptable during network isolation?
- What cardinality limits are required for metrics labels?
- Which logs contain sensitive or regulated data?
- How long should metrics, logs and traces be retained at full resolution?
- What is the authoritative service catalog for ownership and routing?
- Which SLOs represent customer impact rather than internal component health?
- How are alert rules tested before promotion?

## Example acceptance criteria

- A service can be traced from user-facing symptom to infrastructure dependency using correlated telemetry.
- Critical telemetry continues to buffer or recover after a temporary collector/backend interruption.
- Every production alert has a documented owner and response action.
- SLO calculation can be reproduced from stored telemetry.
- High-cardinality or sensitive labels are controlled before ingestion.

## Trade-offs

Centralization improves correlation and governance but can create cost, latency and dependency concentration. More telemetry is not automatically better observability. The architecture should prioritize useful signals, service context and actionable reliability information.
