# Overlay

Visual-debugging overlays, ported from ``FlaUI.Core.Overlay``. Each
[`AutomationBase`](automation_base.md) exposes an ``OverlayManager`` via ``overlay_manager``; it draws
a colored border around a screen rectangle for a short duration (the same mechanism used by
``AutomationElement.draw_highlight``).

::: flaui.core.overlay.OverlayManager
