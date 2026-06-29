"""This module contains unit tests for the pythonnet_bridge module."""
import logging

logger = logging.getLogger(__name__)
import pytest

def test_setup_pythonnet_bridge() -> None:
    """
    Test function to ensure that the Python.NET bridge is properly set up for FlaUI dependencies.

    This function imports the `config` module and the `setup_pythonnet_bridge` function from the `flaui.lib.pythonnet_bridge` module.
    It then checks that the `BIN_HOME` directory specified in the `config.settings` object exists, and calls the `setup_pythonnet_bridge` function.
    If any exceptions are raised during this process, they are logged and the test fails with an appropriate error message.
    """
    try:
        import flaui.lib.config as config
        from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

        assert config.settings.BIN_HOME.exists()
        setup_pythonnet_bridge()
    except Exception as err:
        logger.exception(f"{err}")
        pytest.fail("Failed to setup Python.NET bridge for FlaUI dependencies")


def test_setup_pythonnet_bridge_reraises_on_load_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """A failure while loading a DLL is logged and re-raised (covers the except branch).

    The loop's first ``clr.AddReference`` is patched to raise, so the bridge surfaces the error
    instead of silently swallowing it. No real assemblies are touched.
    """
    import flaui.lib.pythonnet_bridge as bridge

    def _boom(*_args: object, **_kwargs: object) -> None:
        """Simulate a DLL load failure from PythonNet."""
        raise RuntimeError("simulated DLL load failure")

    monkeypatch.setattr(bridge.clr, "AddReference", _boom)

    with pytest.raises(RuntimeError, match="simulated DLL load failure"):
        bridge.setup_pythonnet_bridge()
