from pathlib import Path

import pytest

from conformance_platform.scanner.python_scanner import scan_service


def _write_python_file(
    service_directory: Path,
    relative_path: str,
    content: str,
) -> None:
    file_path = service_directory / "app" / relative_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")


def test_detects_local_layer_dependencies(tmp_path: Path) -> None:
    service_directory = tmp_path / "order-service"

    _write_python_file(
        service_directory,
        "api/orders.py",
        (
            "from app.services.orders import create_order\n"
            "from app.repositories.orders import OrderRepository"
        ),
    )

    result = scan_service(
        service_name="order-service",
        source_path=service_directory,
    )

    assert result.files_scanned == 1
    assert len(result.dependencies) == 2

    target_layers = {
        dependency.target_layer
        for dependency in result.dependencies
    }

    assert target_layers == {"services", "repositories"}
    assert all(
        dependency.source_layer == "api"
        for dependency in result.dependencies
    )


def test_ignores_external_dependencies(tmp_path: Path) -> None:
    service_directory = tmp_path / "payment-service"

    _write_python_file(
        service_directory,
        "services/payments.py",
        (
            "import json\n"
            "import httpx\n"
            "from pathlib import Path"
        ),
    )

    result = scan_service(
        service_name="payment-service",
        source_path=service_directory,
    )

    assert result.files_scanned == 1
    assert result.dependencies == []


def test_rejects_invalid_python(tmp_path: Path) -> None:
    service_directory = tmp_path / "inventory-service"

    _write_python_file(
        service_directory,
        "api/inventory.py",
        "def broken_function(:",
    )

    with pytest.raises(
        SyntaxError,
        match="Cannot scan invalid Python file",
    ):
        scan_service(
            service_name="inventory-service",
            source_path=service_directory,
        )