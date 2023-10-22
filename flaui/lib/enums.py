"""This module contains enums which are used in the FlaUI library."""
from enum import Enum

class UIAutomationTypes(Enum):
    """Lists down UIAutomation types."""
    UIA2 = 'UIA2'
    UIA3 = 'UIA3'

class KnownClassNames(Enum):
    """Lists down all the known element ClassNames."""
    Button = "Button"
    Calendar = "Calendar"
    CheckBox = "CheckBox"
    ComboBox = "ComboBox"
    DataGridView = "DataGridView"
    DateTimePicker = "DateTimePicker"
    Label = "Label"
    Grid = "Grid"
    GridRow = "GridRow"
    GridHeader = "GridHeader"
    GridCell = "GridCell"
    GridHeaderItem = "GridHeaderItem"
    HorizontalScrollBar = "HorizontalScrollBar"
    ListBox = "ListBox"
    Menu = "Menu"
    MenuItem = "MenuItem"
    ProgressBar = "ProgressBar"
    RadioButton = "RadioButton"
    Slider = "Slider"
    Spinner = "Spinner"
    Tab = "Tab"
    TabItem = "TabItem"
    TabControl = "TabControl"
    TextBox = "TextBox"
    Thumb = "Thumb"
    TitleBar = "TitleBar"
    ToggleButton = "ToggleButton"
    Tree = "Tree"
    TreeItem = "TreeItem"
    VerticalScrollBar = "VerticalScrollBar"
    Window = "Window"
