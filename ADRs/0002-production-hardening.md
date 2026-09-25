# ADR-0002: Production hardening
## Decisions
FastAPI defines the edge contract; OpenTelemetry provides trace hooks; Kubernetes owns probes/resources; Helm packages the workload; Terraform owns infrastructure inputs; Trivy and CycloneDX provide CI security/SBOM; Hypothesis and HTTP contract tests protect boundaries; Locust supplies repeatable load traffic.
## Trade-offs
Local deterministic behavior keeps CI reproducible; production externalizes state, secrets, telemetry and autoscaling.
