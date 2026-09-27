"""Validation for experiment manifests before telemetry is accepted."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "0.1.0"
EXPERIMENT_ID_PATTERN = re.compile(r"^TTPT-\d{8}-[A-Z0-9]{4,12}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")

SUPPORTED_TECHNIQUES = {
    "T1059.001": "PowerShell",
    "T1059.003": "Windows Command Shell",
    "T1082": "System Information Discovery",
    "T1033": "System Owner/User Discovery",
    "T1083": "File and Directory Discovery",
    "T1053.005": "Scheduled Task",
}


class ManifestError(ValueError):
    """Raised when experiment metadata violates the project contract."""


def _require_mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ManifestError(f"{name} must be an object")
    return value


def _require_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{name} must be a non-empty string")
    return value.strip()


def _parse_timestamp(value: Any, name: str) -> datetime:
    text = _require_text(value, name)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ManifestError(f"{name} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise ManifestError(f"{name} must include a timezone")
    return parsed


def validate_manifest(data: Any) -> dict[str, Any]:
    """Validate and return an experiment manifest.

    The function intentionally rejects unknown top-level fields so that dataset
    provenance changes are explicit and versioned.
    """

    manifest = _require_mapping(data, "manifest")
    allowed = {
        "schema_version",
        "experiment_id",
        "session_type",
        "technique_id",
        "technique_name",
        "emulation",
        "host",
        "window",
        "authorization",
        "collection",
        "artifacts",
        "notes",
    }
    unknown = sorted(set(manifest) - allowed)
    if unknown:
        raise ManifestError(f"unknown top-level fields: {', '.join(unknown)}")

    required = {
        "schema_version",
        "experiment_id",
        "session_type",
        "host",
        "window",
        "authorization",
        "collection",
        "artifacts",
    }
    missing = sorted(required - set(manifest))
    if missing:
        raise ManifestError(f"missing required fields: {', '.join(missing)}")

    if manifest["schema_version"] != SCHEMA_VERSION:
        raise ManifestError(
            f"schema_version must be {SCHEMA_VERSION!r}, got {manifest['schema_version']!r}"
        )

    experiment_id = _require_text(manifest["experiment_id"], "experiment_id")
    if not EXPERIMENT_ID_PATTERN.fullmatch(experiment_id):
        raise ManifestError("experiment_id must match TTPT-YYYYMMDD-IDENTIFIER")

    session_type = manifest["session_type"]
    if session_type not in {"attack", "benign"}:
        raise ManifestError("session_type must be 'attack' or 'benign'")

    technique_id = manifest.get("technique_id")
    technique_name = manifest.get("technique_name")
    emulation = manifest.get("emulation")
    if session_type == "attack":
        if technique_id not in SUPPORTED_TECHNIQUES:
            supported = ", ".join(sorted(SUPPORTED_TECHNIQUES))
            raise ManifestError(f"unsupported technique_id; expected one of: {supported}")
        expected_name = SUPPORTED_TECHNIQUES[technique_id]
        if technique_name != expected_name:
            raise ManifestError(
                f"technique_name for {technique_id} must be {expected_name!r}"
            )
        emulation_data = _require_mapping(emulation, "emulation")
        if emulation_data.get("framework") not in {"atomic-red-team", "caldera"}:
            raise ManifestError(
                "emulation.framework must be 'atomic-red-team' or 'caldera'"
            )
        _require_text(emulation_data.get("test_id"), "emulation.test_id")
        _require_text(emulation_data.get("variant"), "emulation.variant")
    else:
        if technique_id is not None or technique_name is not None or emulation is not None:
            raise ManifestError(
                "benign sessions must set technique_id, technique_name and emulation to null"
            )

    host = _require_mapping(manifest["host"], "host")
    host_id = _require_text(host.get("host_id"), "host.host_id")
    if not re.fullmatch(r"HOST-[A-Z0-9]{2,12}", host_id):
        raise ManifestError("host.host_id must be an anonymized HOST-* identifier")
    if host.get("platform") != "windows":
        raise ManifestError("host.platform must be 'windows' in the initial scope")
    _require_text(host.get("os_version"), "host.os_version")
    _require_text(host.get("snapshot_id"), "host.snapshot_id")

    window = _require_mapping(manifest["window"], "window")
    started_at = _parse_timestamp(window.get("started_at"), "window.started_at")
    ended_at = _parse_timestamp(window.get("ended_at"), "window.ended_at")
    if ended_at <= started_at:
        raise ManifestError("window.ended_at must be later than window.started_at")

    authorization = _require_mapping(manifest["authorization"], "authorization")
    if authorization.get("scope") != "owned-isolated-lab":
        raise ManifestError("authorization.scope must be 'owned-isolated-lab'")
    if authorization.get("approved") is not True:
        raise ManifestError("authorization.approved must be true")
    if authorization.get("network_isolated") is not True:
        raise ManifestError("authorization.network_isolated must be true")

    collection = _require_mapping(manifest["collection"], "collection")
    sources = collection.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ManifestError("collection.sources must be a non-empty list")
    if "sysmon" not in sources:
        raise ManifestError("collection.sources must include 'sysmon'")
    digest = collection.get("sysmon_config_sha256")
    if not isinstance(digest, str) or not SHA256_PATTERN.fullmatch(digest):
        raise ManifestError("collection.sysmon_config_sha256 must be lowercase SHA-256")

    artifacts = _require_mapping(manifest["artifacts"], "artifacts")
    event_log = _require_text(artifacts.get("event_log"), "artifacts.event_log")
    event_path = Path(event_log)
    if event_path.is_absolute() or ".." in event_path.parts:
        raise ManifestError("artifacts.event_log must be a safe relative path")

    return manifest


def load_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    with manifest_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    return validate_manifest(data)

