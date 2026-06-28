"""Extract the Home Assistant test dependencies required by this integration."""

import sys
from collections import defaultdict
from pathlib import Path

REQUIRED_COMPONENTS = [
    "components.recorder",
    "components.mqtt",
    "components.zeroconf",
    "components.http",
    "components.stream",
    "components.conversation",  # only available after HA>=2023.2
    "components.cloud",
    "components.ffmpeg",  # needed since 2024.1
]

# Home Assistant 2026.6 removed requirements_test_all.txt. Without per-component
# metadata, install the known packages this harness historically needed from the
# flat requirements_all.txt file.
FALLBACK_REQUIREMENT_NAMES = [
    "aiohasupervisor",
    "PyTurboJPEG",
    "av",
    "fnv-hash-fast",
    "ha-ffmpeg",
    "hass-nabucasa",
    "hassil",
    "home-assistant-intents",
    "paho-mqtt",
    "zeroconf",
]


def _dedupe(requirements: list[str]) -> list[str]:
    seen = set()
    deduped = []
    for requirement in requirements:
        if requirement not in seen:
            seen.add(requirement)
            deduped.append(requirement)
    return deduped


def _component_dependencies(lines: list[str]) -> dict[str, list[str]]:
    deps = defaultdict(list)
    components, packages = [], []

    for line in lines:
        line = line.strip()  # noqa: PLW2901

        if line.startswith("# homeassistant."):
            if components and packages:
                for component in components:
                    deps[component].extend(packages)
                components, packages = [], []
            components.append(line.split("# homeassistant.")[1])
        elif components and line:
            packages.append(line)

    if components and packages:
        for component in components:
            deps[component].extend(packages)

    return deps


def _requirements_from_test_all(requirements: Path) -> list[str]:
    deps = _component_dependencies(requirements.read_text().splitlines())
    return _dedupe(
        [package for component in REQUIRED_COMPONENTS for package in deps[component]]
    )


def _requirements_from_all(requirements: Path) -> list[str]:
    wanted_prefixes = tuple(f"{name}==" for name in FALLBACK_REQUIREMENT_NAMES)
    lines = requirements.read_text().splitlines()
    return _dedupe([line for line in lines if line.startswith(wanted_prefixes)])


def dependencies(core_dir: Path = Path("core")) -> list[str]:
    """Return the pinned Home Assistant packages needed by the test harness."""
    requirements_test_all = core_dir / "requirements_test_all.txt"
    requirements_all = core_dir / "requirements_all.txt"

    if requirements_test_all.exists():
        to_install = _requirements_from_test_all(requirements_test_all)
    elif requirements_all.exists():
        print(  # noqa: T201
            "test_dependencies: core/requirements_test_all.txt not found; "
            "resolving required packages from core/requirements_all.txt.",
            file=sys.stderr,
        )
        to_install = _requirements_from_all(requirements_all)
    else:
        print(  # noqa: T201
            "test_dependencies: neither core/requirements_test_all.txt nor "
            "core/requirements_all.txt found; using minimal deps.",
            file=sys.stderr,
        )
        to_install = []

    return [*to_install, "flaky"]


if __name__ == "__main__":
    print(" ".join(dependencies()))  # noqa: T201
