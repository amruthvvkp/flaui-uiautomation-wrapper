from typing import Any

# isort: off
from FlaUI.Core.AutomationElements import (
    AutomationElementExtensions as CSAutomationElementExtensions,
)  # pyright: ignore

# isort: on


class AutomationElementExtensions:
    """Automation Element Extensions to convert generic FlaUI identified objects

    Automation Element Extensions to convert generic FlaUI identified objects casted into proper identified FlaUI objects
    """

    @staticmethod
    def as_button(element: Any) -> Any:
        """Convert as Button

        Converts element as Button

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsButton(element)

    @staticmethod
    def as_calendar(element: Any) -> Any:
        """Convert as Calendar

        Converts element as Calendar

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsCalendar(element)

    @staticmethod
    def as_check_box(element: Any) -> Any:
        """Convert as CheckBox

        Converts element as CheckBox

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsCheckBox(element)

    @staticmethod
    def as_combo_box(element: Any) -> Any:
        """Convert as ComboBox

        Converts element as ComboBox

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsComboBox(element)

    @staticmethod
    def as_data_grid_view(element: Any) -> Any:
        """Convert as DataGridView

        Converts element as DatGridView

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsDataGridView(element)

    @staticmethod
    def as_date_time_picker(element: Any) -> Any:
        """Convert as DateTimePicker

        Converts element as DateTimePicker

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsDateTimePicker(element)

    @staticmethod
    def as_grid(element: Any) -> Any:
        """Convert as Grid

        Converts element as Grid

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsGrid(element)

    @staticmethod
    def as_grid_cell(element: Any) -> Any:
        """Convert as GridCell

        Converts element as GridCell

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsGridCell(element)

    @staticmethod
    def as_grid_header(element: Any) -> Any:
        """Convert as GridHeader

        Converts element as GridHeader

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsGridHeader(element)

    @staticmethod
    def as_grid_header_item(element: Any) -> Any:
        """Convert as GridHeaderItem

        Converts element as GridHeaderItem

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsGridHeaderItem(element)

    @staticmethod
    def as_grid_row(element: Any) -> Any:
        """Convert as GridRow

        Converts element as GridRow

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsGridRow(element)

    @staticmethod
    def as_horizontal_scroll_bar(element: Any) -> Any:
        """Convert as HorizontalScrollBar

        Converts element as HorizontalScrollBar

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsHorizontalScrollBar(element)

    @staticmethod
    def as_label(element: Any) -> Any:
        """Convert as Label

        Converts element as Label

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsLabel(element)

    @staticmethod
    def as_list_box(element: Any) -> Any:
        """Convert as ListBox

        Converts element as ListBox

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsListBox(element)

    @staticmethod
    def as_list_box_item(element: Any) -> Any:
        """Convert as ListBoxItem

        Converts element as ListBoxItem

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsListBoxItem(element)

    @staticmethod
    def as_menu(element: Any) -> Any:
        """Convert as Menu

        Converts element as Menu

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsMenu(element)

    @staticmethod
    def as_menu_item(element: Any) -> Any:
        """Convert as MenuItem

        Converts element as MenuItem

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsMenuItem(element)

    @staticmethod
    def as_progress_bar(element: Any) -> Any:
        """Convert as ProgressBar

        Converts element as ProgressBar

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsProgressBar(element)

    @staticmethod
    def as_radio_button(element: Any) -> Any:
        """Convert as RadioButton

        Converts element as RadioButton

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsRadioButton(element)

    @staticmethod
    def as_slider(element: Any) -> Any:
        """Convert as Slider

        Converts element as Slider

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsSlider(element)

    @staticmethod
    def as_spinner(element: Any) -> Any:
        """Convert as Spinner

        Converts element as Spinner

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsSpinner(element)

    @staticmethod
    def as_tab(element: Any) -> Any:
        """Convert as Tab

        Converts element as Tab

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsTab(element)

    @staticmethod
    def as_tab_item(element: Any) -> Any:
        """Convert as TabItem

        Converts element as TabItem

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsTabItem(element)

    @staticmethod
    def as_text_box(element: Any) -> Any:
        """Convert as TextBox

        Converts element as TextBox

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsTextBox(element)

    @staticmethod
    def as_thumb(element: Any) -> Any:
        """Convert as Thumb

        Converts element as Thumb

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsThumb(element)

    @staticmethod
    def as_title_bar(element: Any) -> Any:
        """Convert as TitleBar

        Converts element as TitleBar

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsTitleBar(element)

    @staticmethod
    def as_toggle_button(element: Any) -> Any:
        """Convert as ToggleButton

        Converts element as ToggleButton

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsToggleButton(element)

    @staticmethod
    def as_tree(element: Any) -> Any:
        """Convert as Tree

        Converts element as Tree

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsTree(element)

    @staticmethod
    def as_tree_item(element: Any) -> Any:
        """Convert as TreeItem

        Converts element as TreeItem

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsTreeItem(element)

    @staticmethod
    def as_vertical_scroll_bar(element: Any) -> Any:
        """Convert as VerticalScrollBar

        Converts element as VerticalScrollBar

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsVerticalScrollBar(element)

    @staticmethod
    def as_window(element: Any) -> Any:
        """Convert as Window

        Converts element as Window

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.AsWindow(element)

    @staticmethod
    def draw_highlight(element: Any) -> Any:
        """Convert as DrawHighlight

        Converts element as Button

        :param element: Generic FlauI element
        """
        return CSAutomationElementExtensions.DrawHighlight(element)
