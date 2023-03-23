from enum import Enum


from FlaUI.Core.Definitions import ControlType as CSControlType  # pyright: ignore


class PropertyConditionFlags(Enum):
    # Note = We cannot import from FlaUI.Core.Definitions import PropertyConditionFlags and
    # use them to build enum here since the first value is None which throws an error on Python
    none = 0
    ignore_case = 1
    match_substring = 2


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
