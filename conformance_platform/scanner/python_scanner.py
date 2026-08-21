import ast
from pathlib import Path

from conformance_platform.scanner.models import (
    DependencyEvidence,
    ServiceScanResult,
)


KNOWN_LAYERS = {
    "api",
    "services",
    "repositories",
    "models",
    "schemas",
}


def _module_name(app_directory: Path, file_path: Path) -> str:
    relative_path = file_path.relative_to(app_directory.parent)
    module_parts = list(relative_path.with_suffix("").parts)

    if module_parts[-1] == "__init__":
        module_parts.pop()

    return ".".join(module_parts)


def _module_layer(module_name: str) -> str | None:
    parts = module_name.split(".")

    if len(parts) >= 2 and parts[0] == "app":
        candidate = parts[1]
        if candidate in KNOWN_LAYERS:
            return candidate

    return None


def _local_imports(tree: ast.AST) -> list[tuple[str, int]]:
    imports: list[tuple[str, int]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "app" or alias.name.startswith("app."):
                    imports.append((alias.name, node.lineno))

        if isinstance(node, ast.ImportFrom):
            module_name = node.module
            if module_name and (
                module_name == "app"
                or module_name.startswith("app.")
            ):
                imports.append((module_name, node.lineno))

    return imports


def scan_service(
    service_name: str,
    source_path: str | Path,
) -> ServiceScanResult:
    service_directory = Path(source_path)
    app_directory = service_directory / "app"

    if not app_directory.is_dir():
        raise FileNotFoundError(
            f"Service app directory not found: {app_directory}"
        )

    dependencies: list[DependencyEvidence] = []
    python_files = sorted(app_directory.rglob("*.py"))

    for file_path in python_files:
        source_code = file_path.read_text(encoding="utf-8")

        try:
            tree = ast.parse(
                source_code,
                filename=str(file_path),
            )
        except SyntaxError as error:
            raise SyntaxError(
                f"Cannot scan invalid Python file: {file_path}"
            ) from error

        source_module = _module_name(app_directory, file_path)
        source_layer = _module_layer(source_module)

        for target_module, line in _local_imports(tree):
            dependencies.append(
                DependencyEvidence(
                    source_file=file_path,
                    line=line,
                    source_module=source_module,
                    target_module=target_module,
                    source_layer=source_layer,
                    target_layer=_module_layer(target_module),
                )
            )

    return ServiceScanResult(
        service_name=service_name,
        source_path=service_directory,
        files_scanned=len(python_files),
        dependencies=dependencies,
    )