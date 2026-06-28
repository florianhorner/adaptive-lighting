from pathlib import Path

from test_dependencies import dependencies


def test_dependencies_parse_requirements_test_all(tmp_path: Path) -> None:
    core = tmp_path / "core"
    core.mkdir()
    (core / "requirements_test_all.txt").write_text(
        """# homeassistant.components.mqtt
paho-mqtt==2.1.0
# homeassistant.components.recorder
fnv-hash-fast==1.6.0
# homeassistant.components.unused
unused-package==1.0.0
""",
    )

    assert dependencies(core) == [
        "fnv-hash-fast==1.6.0",
        "paho-mqtt==2.1.0",
        "flaky",
    ]


def test_dependencies_fall_back_to_requirements_all(tmp_path: Path) -> None:
    core = tmp_path / "core"
    core.mkdir()
    (core / "requirements_all.txt").write_text(
        """aiohasupervisor==0.4.3
paho-mqtt==2.1.0
unused-package==1.0.0
zeroconf==0.149.16
""",
    )

    assert dependencies(core) == [
        "aiohasupervisor==0.4.3",
        "paho-mqtt==2.1.0",
        "zeroconf==0.149.16",
        "flaky",
    ]


def test_dependencies_use_minimal_fallback_without_core_aggregate_files(
    tmp_path: Path,
) -> None:
    core = tmp_path / "core"
    core.mkdir()

    assert dependencies(core) == ["flaky"]
