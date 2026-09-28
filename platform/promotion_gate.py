"""Model promotion gate."""


REQUIRED = ("security", "quality", "cost", "provenance")


def can_promote(evidence: dict[str, bool], canary_ready: bool) -> bool:
    return all(evidence.get(k, False) for k in REQUIRED) and canary_ready
