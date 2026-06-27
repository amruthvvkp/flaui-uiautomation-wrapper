"""
This module contains wrapper classes for the C# namespace FlaUI.Core.Definitions.
It defines several enums for different types of controls in Microsoft UI Automation."""

from enum import Enum

# Wrapper class for the C# namespace FlaUI.Core.Definitions
from FlaUI.Core.Definitions import (  # pyright: ignore
    AutomationElementMode as CSAutomationElementMode,
    ControlType as CSControlType,
    DockPosition as CSDockPosition,
    ExpandCollapseState as CSExpandCollapseState,
    PropertyConditionFlags as CSPropertyConditionFlags,
    RowOrColumnMajor as CSRowOrColumnMajor,
    ScrollAmount as CSScrollAmount,
    SupportedTextSelection as CSSupportedTextSelection,
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
