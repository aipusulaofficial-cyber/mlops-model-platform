# AIPusula Platform Integration — Model Lifecycle

## Promotion lifecycle
`REGISTERED -> SECURITY_VALIDATED -> EVALUATED -> COST_VALIDATED -> STAGING -> CANARY -> PRODUCTION -> ARCHIVED`

Every transition requires a recorded actor/system, timestamp, candidate version and evidence reference.

## Persistence contract
Keep the storage interface independent from the database. SQLite is suitable for local development; production persistence must support transactional updates, concurrent promotion protection, idempotency and audit history.

## Promotion gate
A model cannot advance without:
- security validation
- quality evaluation
- cost validation
- required tests
- provenance/SBOM evidence
- deployment readiness

## Canary
Canary promotion must have explicit start/stop criteria and rollback evidence. Never treat a canary as production by convention.

## Integration points
- ai-evaluation-platform: quality evidence
- secure-ai-gateway: model policy
- distributed-ai-inference-platform: runtime deployment
- ai-cost-optimization-platform: cost evidence
- ai-observability-platform: canary telemetry
- supply-chain pipeline: SBOM/provenance/signature verification

## Engineering standard
Code -> Contract -> Test -> Security -> Runtime -> Observability -> Deployment -> Evidence
