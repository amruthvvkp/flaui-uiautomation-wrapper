# Wrapper class for the C# namespace FlaUI.Core.Definitions
from enum import Enum

from FlaUI.Core.Definitions import ControlType as CSControlType  # pyright: ignore
from FlaUI.Core.Definitions import ExpandCollapseState as CSExpandCollapseState  # pyright: ignore
from FlaUI.Core.Definitions import PropertyConditionFlags as CSPropertyConditionFlags  # pyright: ignore
from FlaUI.Core.Definitions import RowOrColumnMajor as CSRowOrColumnMajor  # pyright: ignore
from FlaUI.Core.Definitions import ToggleState as CSToggleState  # pyright: ignore

class PropertyConditionFlags(Enum):
    """Optional flags that are used when checking the property."""
    none = getattr(CSPropertyConditionFlags, "None") # We need to use getattr here because Python.Net doesn't like the None value
    ignore_case = CSPropertyConditionFlags.IgnoreCase
    match_substring = CSPropertyConditionFlags.MatchSubstring


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
    Collapsed = CSExpandCollapseState.Collapsed
    Expanded = CSExpandCollapseState.Expanded
    PartiallyExpanded = CSExpandCollapseState.PartiallyExpanded
    LeafNode = CSExpandCollapseState.LeafNode


class RowOrColumnMajor(Enum):
    RowMajor = CSRowOrColumnMajor.RowMajor
    ColumnMajor = CSRowOrColumnMajor.ColumnMajor
    Indeterminate = CSRowOrColumnMajor.Indeterminate
