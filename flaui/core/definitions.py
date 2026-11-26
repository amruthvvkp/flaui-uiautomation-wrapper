"""
This module contains wrapper classes for the C# namespace FlaUI.Core.Definitions.
It defines several enums for different types of controls in Microsoft UI Automation."""

from enum import Enum, IntFlag
from typing import Any, Dict, Optional, Type, Union

# Wrapper class for the C# namespace FlaUI.Core.Definitions
from FlaUI.Core.Definitions import (  # pyright: ignore
    AnnotationType as CSAnnotationType,
    AutomationElementMode as CSAutomationElementMode,
    CoalesceEventsOptions as CSCoalesceEventsOptions,
    ConnectionRecoveryBehaviorOptions as CSConnectionRecoveryBehaviorOptions,
    ControlType as CSControlType,
    DockPosition as CSDockPosition,
    ExpandCollapseState as CSExpandCollapseState,
    FrameworkIds as CSFrameworkIds,
    HeadingLevel as CSHeadingLevel,
    LandmarkType as CSLandmarkType,
    LiveSetting as CSLiveSetting,
    NotificationKind as CSNotificationKind,
    NotificationProcessing as CSNotificationProcessing,
    OrientationType as CSOrientationType,
    PropertyConditionFlags as CSPropertyConditionFlags,
    RowOrColumnMajor as CSRowOrColumnMajor,
    ScrollAmount as CSScrollAmount,
    StructureChangeType as CSStructureChangeType,
    StyleType as CSStyleType,
    SupportedTextSelection as CSSupportedTextSelection,
    SynchronizedInputType as CSSynchronizedInputType,
    TextEditChangeType as CSTextEditChangeType,
    TextPatternRangeEndpoint as CSTextPatternRangeEndpoint,
    TextUnit as CSTextUnit,
    ToggleState as CSToggleState,
    TreeScope as CSTreeScope,
    TreeTraversalOptions as CSTreeTraversalOptions,
    WindowInteractionState as CSWindowInteractionState,
    WindowVisualState as CSWindowVisualState,
    ZoomUnit as CSZoomUnit,
)


class AutomationElementMode(Enum):
    """Contains values that specify the type of reference to use when returning UI Automation elements."""

    None_ = getattr(
        CSAutomationElementMode, "None"
    )  # Specifies returned elements have no reference to UI and contain only cached information
    Full = CSAutomationElementMode.Full  # Specifies returned elements have a full reference to the underlying UI


class PropertyConditionFlags(Enum):
    """Optional flags that are used when checking the property."""

    None_ = getattr(
        CSPropertyConditionFlags, "None"
    )  # We need to use getattr here because Python.Net doesn't like the None value
    IgnoreCase = CSPropertyConditionFlags.IgnoreCase
    MatchSubstring = CSPropertyConditionFlags.MatchSubstring


class ControlType(Enum):
    """Types of controls in Microsoft UI Automation."""

    AppBar = CSControlType.AppBar
    Button = CSControlType.Button
    Calendar = CSControlType.Calendar
    CheckBox = CSControlType.CheckBox
    ComboBox = CSControlType.ComboBox
    CompareTo = CSControlType.CompareTo
    Custom = CSControlType.Custom
    DataGrid = CSControlType.DataGrid
    DataItem = CSControlType.DataItem
    Document = CSControlType.Document
    Edit = CSControlType.Edit
    Equals = CSControlType.Equals
    Finalize = CSControlType.Finalize
    Format = CSControlType.Format
    GetHashCode = CSControlType.GetHashCode
    GetName = CSControlType.GetName
    GetNames = CSControlType.GetNames
    GetType = CSControlType.GetType
    GetTypeCode = CSControlType.GetTypeCode
    GetUnderlyingType = CSControlType.GetUnderlyingType
    GetValues = CSControlType.GetValues
    Group = CSControlType.Group
    HasFlag = CSControlType.HasFlag
    Header = CSControlType.Header
    HeaderItem = CSControlType.HeaderItem
    Hyperlink = CSControlType.Hyperlink
    Image = CSControlType.Image
    IsDefined = CSControlType.IsDefined
    List = CSControlType.List
    ListItem = CSControlType.ListItem
    MemberwiseClone = CSControlType.MemberwiseClone
    Menu = CSControlType.Menu
    MenuBar = CSControlType.MenuBar
    MenuItem = CSControlType.MenuItem
    Overloads = CSControlType.Overloads
    Pane = CSControlType.Pane
    Parse = CSControlType.Parse
    ProgressBar = CSControlType.ProgressBar
    RadioButton = CSControlType.RadioButton
    ReferenceEquals = CSControlType.ReferenceEquals
    ScrollBar = CSControlType.ScrollBar
    SemanticZoom = CSControlType.SemanticZoom
    Separator = CSControlType.Separator
    Slider = CSControlType.Slider
    Spinner = CSControlType.Spinner
    SplitButton = CSControlType.SplitButton
    StatusBar = CSControlType.StatusBar
    Tab = CSControlType.Tab
    TabItem = CSControlType.TabItem
    Table = CSControlType.Table
    Text = CSControlType.Text
    Thumb = CSControlType.Thumb
    TitleBar = CSControlType.TitleBar
    ToObject = CSControlType.ToObject
    ToString = CSControlType.ToString
    ToolBar = CSControlType.ToolBar
    ToolTip = CSControlType.ToolTip
    Tree = CSControlType.Tree
    TreeItem = CSControlType.TreeItem
    TryParse = CSControlType.TryParse
    Unknown = CSControlType.Unknown
    Window = CSControlType.Window


class ToggleState(Enum):
    """Contains values that specify the toggle state of a Microsoft UI Automation element that implements the TogglePattern"""

    Off = CSToggleState.Off
    On = CSToggleState.On
    Indeterminate = CSToggleState.Indeterminate


class ExpandCollapseState(Enum):
    """Contains values that specify the expand/collapse state of a Microsoft UI Automation element that implements the ExpandCollapsePattern."""

    Collapsed = CSExpandCollapseState.Collapsed
    Expanded = CSExpandCollapseState.Expanded
    PartiallyExpanded = CSExpandCollapseState.PartiallyExpanded
    LeafNode = CSExpandCollapseState.LeafNode


class RowOrColumnMajor(Enum):
    """Contains values that specify the row/column major order of items in a container."""

    RowMajor = CSRowOrColumnMajor.RowMajor
    ColumnMajor = CSRowOrColumnMajor.ColumnMajor
    Indeterminate = CSRowOrColumnMajor.Indeterminate


class ScrollAmount(Enum):
    """Contains values that specify the direction and distance to scroll."""

    LargeDecrement = CSScrollAmount.LargeDecrement
    SmallDecrement = CSScrollAmount.SmallDecrement
    NoAmount = CSScrollAmount.NoAmount
    LargeIncrement = CSScrollAmount.LargeIncrement
    SmallIncrement = CSScrollAmount.SmallIncrement


class TreeScope(Enum):
    """Contains values that specify the scope of various operations in the Microsoft UI Automation tree."""

    None_ = getattr(CSTreeScope, "None")
    Element = CSTreeScope.Element
    Children = CSTreeScope.Children
    Descendants = CSTreeScope.Descendants
    Subtree = CSTreeScope.Subtree
    Parent = CSTreeScope.Parent
    Ancestors = CSTreeScope.Ancestors


class TreeTraversalOptions(Enum):
    """Contains values that specify the traversal options for the tree walker."""

    Default = CSTreeTraversalOptions.Default
    PostOrder = CSTreeTraversalOptions.PostOrder
    LastToFirstOrder = CSTreeTraversalOptions.LastToFirstOrder


class WindowVisualState(Enum):
    """Contains values that specify the visual state of a window."""

    Normal = CSWindowVisualState.Normal
    Maximized = CSWindowVisualState.Maximized
    Minimized = CSWindowVisualState.Minimized


class WindowInteractionState(Enum):
    """Contains values that specify the current state of a window for user interaction."""

    Running = CSWindowInteractionState.Running
    Closing = CSWindowInteractionState.Closing
    ReadyForUserInteraction = CSWindowInteractionState.ReadyForUserInteraction
    BlockedByModalWindow = CSWindowInteractionState.BlockedByModalWindow
    NotResponding = CSWindowInteractionState.NotResponding


class DockPosition(Enum):
    """Contains values that specify the dock position of an element within a docking container."""

    Top = CSDockPosition.Top
    Left = CSDockPosition.Left
    Bottom = CSDockPosition.Bottom
    Right = CSDockPosition.Right
    Fill = CSDockPosition.Fill
    None_ = getattr(CSDockPosition, "None")


class ZoomUnit(Enum):
    """Contains values that specify the amount to zoom on a control."""

    NoAmount = CSZoomUnit.NoAmount
    LargeDecrement = CSZoomUnit.LargeDecrement
    SmallDecrement = CSZoomUnit.SmallDecrement
    LargeIncrement = CSZoomUnit.LargeIncrement
    SmallIncrement = CSZoomUnit.SmallIncrement


class SupportedTextSelection(Enum):
    """Contains values that specify the supported text selection attribute of a text control."""

    None_ = getattr(CSSupportedTextSelection, "None")
    Single = CSSupportedTextSelection.Single
    Multiple = CSSupportedTextSelection.Multiple


class TextPatternRangeEndpoint(Enum):
    """Contains values that specify the endpoints of a text range."""

    Start = CSTextPatternRangeEndpoint.Start
    End = CSTextPatternRangeEndpoint.End


class TextUnit(Enum):
    """Contains values that specify units of text for the purposes of navigation."""

    Character = CSTextUnit.Character
    Format = CSTextUnit.Format
    Word = CSTextUnit.Word
    Line = CSTextUnit.Line
    Paragraph = CSTextUnit.Paragraph
    Page = CSTextUnit.Page
    Document = CSTextUnit.Document


class SynchronizedInputType(Enum):
    """Contains values that specify the type of synchronized input to listen for."""

    KeyUp = CSSynchronizedInputType.KeyUp
    KeyDown = CSSynchronizedInputType.KeyDown
    LeftMouseUp = CSSynchronizedInputType.LeftMouseUp
    LeftMouseDown = CSSynchronizedInputType.LeftMouseDown
    RightMouseUp = CSSynchronizedInputType.RightMouseUp
    RightMouseDown = CSSynchronizedInputType.RightMouseDown


class AnnotationType(Enum):
    """Contains the annotation types FlaUI exposes through the Annotation pattern.

    The member values are FlaUI's own enum values. UIA's raw annotation type ids (``60000`` and up, as
    returned by ``Properties.annotation_types``) are a different number space and are not converted.
    """

    AdvancedProofingIssue = CSAnnotationType.AdvancedProofingIssue
    Author = CSAnnotationType.Author
    CircularReferenceError = CSAnnotationType.CircularReferenceError
    Comment = CSAnnotationType.Comment
    ConflictingChange = CSAnnotationType.ConflictingChange
    DataValidationError = CSAnnotationType.DataValidationError
    DeletionChange = CSAnnotationType.DeletionChange
    EditingLockedChange = CSAnnotationType.EditingLockedChange
    Endnote = CSAnnotationType.Endnote
    ExternalChange = CSAnnotationType.ExternalChange
    Footer = CSAnnotationType.Footer
    Footnote = CSAnnotationType.Footnote
    FormatChange = CSAnnotationType.FormatChange
    FormulaError = CSAnnotationType.FormulaError
    GrammarError = CSAnnotationType.GrammarError
    Header = CSAnnotationType.Header
    Highlighted = CSAnnotationType.Highlighted
    InsertionChange = CSAnnotationType.InsertionChange
    Mathematics = CSAnnotationType.Mathematics
    MoveChange = CSAnnotationType.MoveChange
    Sensitive = CSAnnotationType.Sensitive
    SpellingError = CSAnnotationType.SpellingError
    TrackChanges = CSAnnotationType.TrackChanges
    Unknown = CSAnnotationType.Unknown
    UnsyncedChange = CSAnnotationType.UnsyncedChange


class CoalesceEventsOptions(Enum):
    """Contains values that specify whether the automation coalesces events (``AutomationBase.coalesce_events``)."""

    Disabled = CSCoalesceEventsOptions.Disabled
    Enabled = CSCoalesceEventsOptions.Enabled


class ConnectionRecoveryBehaviorOptions(Enum):
    """Contains values that specify whether the automation recovers lost connections automatically."""

    Disabled = CSConnectionRecoveryBehaviorOptions.Disabled
    Enabled = CSConnectionRecoveryBehaviorOptions.Enabled


class HeadingLevel(Enum):
    """Contains values that describe the heading level of an element (``Properties.heading_level``)."""

    None_ = getattr(CSHeadingLevel, "None")
    Level1 = CSHeadingLevel.Level1
    Level2 = CSHeadingLevel.Level2
    Level3 = CSHeadingLevel.Level3
    Level4 = CSHeadingLevel.Level4
    Level5 = CSHeadingLevel.Level5
    Level6 = CSHeadingLevel.Level6
    Level7 = CSHeadingLevel.Level7
    Level8 = CSHeadingLevel.Level8
    Level9 = CSHeadingLevel.Level9


class LandmarkType(Enum):
    """Contains values that describe the landmark type of an element (``Properties.landmark_type``)."""

    CustomLandmark = CSLandmarkType.CustomLandmark
    FormLandmark = CSLandmarkType.FormLandmark
    MainLandmark = CSLandmarkType.MainLandmark
    NavigationLandmark = CSLandmarkType.NavigationLandmark
    SearchLandmark = CSLandmarkType.SearchLandmark


class LiveSetting(Enum):
    """Contains values that describe how a live region announces changes (``Properties.live_setting``)."""

    Off = CSLiveSetting.Off
    Polite = CSLiveSetting.Polite
    Assertive = CSLiveSetting.Assertive


class NotificationKind(Enum):
    """Contains values that describe the kind of a notification event."""

    ItemAdded = CSNotificationKind.ItemAdded
    ItemRemoved = CSNotificationKind.ItemRemoved
    ActionCompleted = CSNotificationKind.ActionCompleted
    ActionAborted = CSNotificationKind.ActionAborted
    Other = CSNotificationKind.Other


class NotificationProcessing(Enum):
    """Contains values that describe how a notification event should be processed."""

    ImportantAll = CSNotificationProcessing.ImportantAll
    ImportantMostRecent = CSNotificationProcessing.ImportantMostRecent
    All = CSNotificationProcessing.All
    MostRecent = CSNotificationProcessing.MostRecent
    CurrentThenMostRecent = CSNotificationProcessing.CurrentThenMostRecent


class OrientationType(Enum):
    """Contains values that specify the orientation of a control (``Properties.orientation``)."""

    None_ = getattr(CSOrientationType, "None")
    Horizontal = CSOrientationType.Horizontal
    Vertical = CSOrientationType.Vertical


class StructureChangeType(Enum):
    """Contains values that describe the change passed to a structure-changed event handler."""

    ChildAdded = CSStructureChangeType.ChildAdded
    ChildRemoved = CSStructureChangeType.ChildRemoved
    ChildrenInvalidated = CSStructureChangeType.ChildrenInvalidated
    ChildrenBulkAdded = CSStructureChangeType.ChildrenBulkAdded
    ChildrenBulkRemoved = CSStructureChangeType.ChildrenBulkRemoved
    ChildrenReordered = CSStructureChangeType.ChildrenReordered


class StyleType(Enum):
    """Contains values that describe the visual style of an element (``StylesPattern.style``)."""

    BulletedList = CSStyleType.BulletedList
    Custom = CSStyleType.Custom
    Emphasis = CSStyleType.Emphasis
    Heading1 = CSStyleType.Heading1
    Heading2 = CSStyleType.Heading2
    Heading3 = CSStyleType.Heading3
    Heading4 = CSStyleType.Heading4
    Heading5 = CSStyleType.Heading5
    Heading6 = CSStyleType.Heading6
    Heading7 = CSStyleType.Heading7
    Heading8 = CSStyleType.Heading8
    Heading9 = CSStyleType.Heading9
    Normal = CSStyleType.Normal
    NumberedList = CSStyleType.NumberedList
    Quote = CSStyleType.Quote
    Subtitle = CSStyleType.Subtitle
    Title = CSStyleType.Title


class TextEditChangeType(Enum):
    """Contains values that describe the change passed to a text-edit text-changed event handler."""

    None_ = getattr(CSTextEditChangeType, "None")
    AutoCorrect = CSTextEditChangeType.AutoCorrect
    Composition = CSTextEditChangeType.Composition
    CompositionFinalized = CSTextEditChangeType.CompositionFinalized


class VisualEffects(IntFlag):
    """Contains the visual effects applied to an element (``Properties.visual_effects``).

    The C# enum is a ``[Flags]`` enum, so this is an :class:`~enum.IntFlag` whose values are the C# integer
    values: combined effects such as ``VisualEffects.Shadow | VisualEffects.Glow`` round-trip correctly.
    """

    None_ = 0
    Shadow = 1
    Reflection = 2
    Glow = 4
    SoftEdges = 8
    Bevel = 16


class FrameworkIds:
    """Python port of the C# static helper ``FlaUI.Core.Definitions.FrameworkIds``.

    It maps between a :class:`~flaui.core.framework_types.FrameworkType` and the UIA ``FrameworkId`` string
    (``"WPF"``, ``"WinForm"``, ``"Win32"``, ``"XAML"``, ``"Qt"``), delegating to FlaUI for exact parity.
    """

    @staticmethod
    def convert(value: Any) -> Any:
        """Convert a framework id string to a ``FrameworkType``, or a ``FrameworkType`` to its id string.

        :param value: A UIA framework id string, or a Python or C# ``FrameworkType``.
        :return: The matching Python ``FrameworkType`` for a string input (``FrameworkType.Unknown`` when the
            id is not recognised), otherwise the framework id string (``None`` for ``FrameworkType.Unknown``,
            ``""`` for ``FrameworkType.none``).
        """
        from flaui.core.framework_types import FrameworkType

        if isinstance(value, str):
            return to_python_enum(CSFrameworkIds.Convert(value), FrameworkType)
        if isinstance(value, FrameworkType):
            if value is FrameworkType.none:
                return ""
            value = value.value
        return CSFrameworkIds.Convert(value)


#: C# enum type name -> Python enum, for the enums converted automatically at the interop boundary.
_CS_ENUM_TYPES: Dict[str, Type[Enum]] = {
    "FlaUI.Core.Definitions.AnnotationType": AnnotationType,
    "FlaUI.Core.Definitions.CoalesceEventsOptions": CoalesceEventsOptions,
    "FlaUI.Core.Definitions.ConnectionRecoveryBehaviorOptions": ConnectionRecoveryBehaviorOptions,
    "FlaUI.Core.Definitions.HeadingLevel": HeadingLevel,
    "FlaUI.Core.Definitions.LandmarkType": LandmarkType,
    "FlaUI.Core.Definitions.LiveSetting": LiveSetting,
    "FlaUI.Core.Definitions.NotificationKind": NotificationKind,
    "FlaUI.Core.Definitions.NotificationProcessing": NotificationProcessing,
    "FlaUI.Core.Definitions.OrientationType": OrientationType,
    "FlaUI.Core.Definitions.StructureChangeType": StructureChangeType,
    "FlaUI.Core.Definitions.StyleType": StyleType,
    "FlaUI.Core.Definitions.TextEditChangeType": TextEditChangeType,
    "FlaUI.Core.Definitions.VisualEffects": VisualEffects,
}


def to_python_enum(value: Any, enum_type: Optional[Type[Enum]] = None) -> Any:
    """Convert a C# ``FlaUI.Core.Definitions`` enum value to its Python enum.

    :param value: The value returned by C#. Python enum members and values of unmapped types pass through.
    :param enum_type: The Python enum to convert to; inferred from the C# type of ``value`` when omitted.
    :return: The matching Python enum member, or ``value`` unchanged when no mapping applies. A C# value
        outside the enum's defined members (for example ``default(HeadingLevel)`` = ``0``, which FlaUI's
        ``ValueOrDefault`` returns for an unsupported property) is also returned unchanged.
    """
    if value is None or isinstance(value, Enum):
        return value
    if enum_type is None:
        get_type = getattr(value, "GetType", None)
        if get_type is None:
            return value
        enum_type = _CS_ENUM_TYPES.get(str(get_type().FullName))
        if enum_type is None:
            return value
    try:
        if issubclass(enum_type, IntFlag):
            return enum_type(int(value))
        return enum_type(value)
    except ValueError:
        return value


def to_cs_enum(value: Union[Enum, Any]) -> Any:
    """Convert a Python enum member to the C# value FlaUI expects.

    :param value: A Python enum member from this module, or a raw C# value (passed through).
    :return: The C# enum value.
    """
    if isinstance(value, VisualEffects):
        from System import Enum as CSEnum  # pyright: ignore

        from FlaUI.Core.Definitions import VisualEffects as CSVisualEffects  # pyright: ignore

        return CSEnum.ToObject(CSVisualEffects, int(value))
    if isinstance(value, Enum):
        return value.value
    return value
