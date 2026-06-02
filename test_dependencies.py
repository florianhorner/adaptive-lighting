"""Extracts the dependencies of the components required for testing."""

import sys
from collections import defaultdict
from pathlib import Path

deps = defaultdict(list)
components, packages = [], []

requirements = Path("core") / "requirements_test_all.txt"

if requirements.exists():
    with requirements.open() as f:
        lines = f.readlines()
else:
    # home-assistant/core removed requirements_test_all.txt from its `dev`
    # branch. Without it we cannot resolve per-component test deps, so fall
    # back to a minimal set (just `flaky`, appended below) instead of crashing
    # with FileNotFoundError. The `dev` matrix leg is a non-blocking
    # early-warning leg; tagged stable releases still ship the file and
    # resolve the full dependency set.
    print(  # noqa: T201
        "test_dependencies: core/requirements_test_all.txt not found; "
        "using minimal deps (expected on HA core 'dev').",
        file=sys.stderr,
    )
    lines = []

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

# The last batch of components and packages
if components and packages:
    for component in components:
        deps[component].extend(packages)

required = [
    "components.recorder",
    "components.mqtt",
    "components.zeroconf",
    "components.http",
    "components.stream",
    "components.conversation",  # only available after HA≥2023.2
    "components.cloud",
    "components.ffmpeg",  # needed since 2024.1
]
to_install = [package for r in required for package in deps[r]]
to_install.append("flaky")

print(" ".join(to_install))  # noqa: T201
