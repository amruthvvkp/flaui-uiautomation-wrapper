# Definitions

Python ports of the C# `FlaUI.Core.Definitions` enums (`ControlType`, `ToggleState`, `TreeScope`,
`OrientationType`, `HeadingLevel`, `LiveSetting`, ...). Member names and values mirror C# one to one:
`None` members are spelled `None_` because `None` is a Python keyword.

Values FlaUI hands back are converted at the boundary, so you can assert against the Python enums:

- enum-typed element properties (`Properties.orientation`, `heading_level`, `landmark_type`,
  `live_setting`, `visual_effects`) and pattern properties (`AnnotationPattern.annotation_type`,
  `StylesPattern.style`) return Python enums from `AutomationProperty.value` / `value_or_default`;
- `AutomationBase.coalesce_events` / `connection_recovery_behavior` read and accept
  `CoalesceEventsOptions` / `ConnectionRecoveryBehaviorOptions`;
- structure-changed, notification and text-edit event callbacks receive `StructureChangeType`,
  `NotificationKind` / `NotificationProcessing` and `TextEditChangeType`.

`VisualEffects` is a `[Flags]` enum in C#, so it is an `IntFlag` in Python and combined effects
round-trip. `FrameworkIds.convert` maps between a `FrameworkType` and the UIA `FrameworkId` string.

::: flaui.core.definitions
