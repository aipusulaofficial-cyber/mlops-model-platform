# Principal Engineering Contract

## Scope
This document defines the engineering decisions that make this repository reviewable as a production-oriented reference implementation.

## Core boundary
**Primary concern:** Model lifecycle.

Treat model metadata, validation, promotion, and serving boundaries independently; make lifecycle transitions explicit; preserve provenance; validate promotion inputs; keep deployment adapters replaceable.

## Non-functional requirements
- **Determinism:** core behavior is reproducible in tests without live external services.
- **Failure semantics:** expected failure classes are explicit and observable; hidden retries are avoided.
- **Security:** untrusted inputs are validated; workloads run non-root with least privilege; deployment images are version-pinned.
- **Supply-chain security:** GitHub Actions are pinned to immutable commit SHAs; workflow tokens use least-privilege permissions.
- **Operability:** health/readiness signals are exposed and enough context is preserved to diagnose failures.
- **Change safety:** CI, production tests, and security/SBOM scans are release gates.

## Review checklist
- [x] Public contracts are validated.
- [x] Domain policy is independent from infrastructure adapters.
- [x] Failure and retry behavior is explicit.
- [x] Resource limits are bounded where work can grow.
- [x] Tests cover happy path, invalid input, and representative failure paths.
- [x] Security-sensitive decisions are auditable.
- [x] Workflows declare least-privilege permissions and timeouts.
- [x] Third-party Actions are pinned to full commit SHAs.
- [x] Kubernetes/Helm/Terraform workloads enforce non-root, seccomp RuntimeDefault, no privilege escalation, read-only root filesystem, and dropped capabilities.
- [x] Deployment images avoid mutable latest tags.
- [x] Dependabot tracks Python and GitHub Actions updates.
- [x] Architecture trade-offs are documented rather than implied.

## Evidence boundary
GREEN means the repository's configured CI, production-test, and security/SBOM gates pass on the current main commit. This is repository-level engineering evidence, not a claim of environment-independent production certification.

## What this is not
This is a reference implementation. Production deployment still requires environment-specific SLOs, capacity planning, secrets management, dependency hardening, and operational ownership.
