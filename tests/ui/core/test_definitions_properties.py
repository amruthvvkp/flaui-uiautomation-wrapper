"""UI tests: element properties backed by ``FlaUI.Core.Definitions`` enums come back as Python enums (GH-157)."""

import pytest

from flaui.core.definitions import FrameworkIds, LiveSetting, OrientationType, VisualEffects
from flaui.core.framework_types import FrameworkType
from flaui.lib.enums import UIAutomationTypes

from tests.test_utilities.elements.winforms_application import WinFormsApplicationElements
from tests.test_utilities.elements.wpf_application import WPFApplicationElements

UIA2_ONLY_MATRIX = {"ui_automation_type": [UIAutomationTypes.UIA2], "test_app_type": ["WinForms", "WPF"]}
UIA2_REASON = "LiveSetting / VisualEffects are UIA3-only properties; UIA2 raises NotSupportedByFramework"


class TestDefinitionEnumProperties:
    """Read enum-typed properties on the UIA2/UIA3 x WinForms/WPF matrix."""

    def test_slider_orientation(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, test_application_type: str
    ) -> None:
        """The slider reports an :class:`OrientationType` (WPF's slider peer does not expose one)."""
        orientation = test_application.simple_controls_tab.slider.properties.orientation.value
        expected = OrientationType.None_ if test_application_type == "WPF" else OrientationType.Horizontal
        assert orientation is expected

    @pytest.mark.skip_if_matrix(UIA2_ONLY_MATRIX, reason=UIA2_REASON)
    def test_live_setting_defaults_to_off(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """A control that is not a live region reports :attr:`LiveSetting.Off`."""
        live_setting = test_application.simple_controls_tab.slider.properties.live_setting.value_or_default
        assert live_setting is LiveSetting.Off

    @pytest.mark.skip_if_matrix(UIA2_ONLY_MATRIX, reason=UIA2_REASON)
    def test_visual_effects_default_to_none(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements
    ) -> None:
        """The main window has no visual effects."""
        effects = test_application.main_window.properties.visual_effects.value_or_default
        assert isinstance(effects, VisualEffects)
        assert effects == VisualEffects.None_

    def test_framework_id_converts(
        self, test_application: WinFormsApplicationElements | WPFApplicationElements, test_application_type: str
    ) -> None:
        """``FrameworkIds.convert`` maps the window's ``FrameworkId`` to the application's framework."""
        framework_id = test_application.main_window.properties.framework_id.value
        expected = FrameworkType.Wpf if test_application_type == "WPF" else FrameworkType.WinForms
        assert FrameworkIds.convert(framework_id) is expected
