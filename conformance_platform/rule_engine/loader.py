from pathlib import Path
from typing import Any

import yaml

from conformance_platform.rule_engine.models import ArchitectureRules


def load_rules(path: str | Path) -> ArchitectureRules:
    rule_path = Path(path)

    if not rule_path.is_file():
        raise FileNotFoundError(
            f"Architecture rule file not found: {rule_path}"
        )

    raw_content = rule_path.read_text(encoding="utf-8")
    parsed: Any = yaml.safe_load(raw_content)

    if not isinstance(parsed, dict):
        raise TypeError(
        "Architecture rule file must contain a YAML object"
    )

    return ArchitectureRules.model_validate(parsed)