from datetime import date
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Severity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ApplicationConfig(StrictModel):
    name: str = Field(min_length=1)
    language: str = Field(min_length=1)
    architecture: str = Field(min_length=1)


class ServiceRule(StrictModel):
    source_path: str = Field(min_length=1)
    database: str = Field(min_length=1)
    allowed_calls: list[str] = Field(default_factory=list)


class LayerRule(StrictModel):
    allowed_imports: list[str] = Field(default_factory=list)


class PolicyRule(StrictModel):
    enabled: bool = True
    severity: Severity


class PolicyCollection(StrictModel):
    unauthorized_service_call: PolicyRule
    cross_service_database_access: PolicyRule
    layer_violation: PolicyRule
    circular_dependency: PolicyRule


class ArchitectureException(StrictModel):
    rule: str = Field(min_length=1)
    source: str = Field(min_length=1)
    target: str | None = None
    reason: str = Field(min_length=1)
    owner: str = Field(min_length=1)
    expires_on: date


class ArchitectureRules(StrictModel):
    version: str = Field(min_length=1)
    application: ApplicationConfig
    services: dict[str, ServiceRule] = Field(min_length=1)
    layer_rules: dict[str, LayerRule] = Field(min_length=1)
    policies: PolicyCollection
    exceptions: list[ArchitectureException] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_service_references(self) -> "ArchitectureRules":
        known_services = set(self.services)

        source_paths = [
            service.source_path for service in self.services.values()
        ]
        if len(source_paths) != len(set(source_paths)):
            raise ValueError("Every service must have a unique source_path")

        databases = [service.database for service in self.services.values()]
        if len(databases) != len(set(databases)):
            raise ValueError("Every service must own a unique database")

        for service_name, rule in self.services.items():
            if service_name in rule.allowed_calls:
                raise ValueError(
                    f"{service_name} cannot call itself"
                )

            unknown_targets = set(rule.allowed_calls) - known_services
            if unknown_targets:
                targets = ", ".join(sorted(unknown_targets))
                raise ValueError(
                    f"{service_name} references unknown services: {targets}"
                )

        return self