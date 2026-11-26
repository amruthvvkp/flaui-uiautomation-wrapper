# Spinner

!!! warning "WinForms NumericUpDown can be missing from the tree"
    On some Windows 11 builds the WinForms `NumericUpDown` never shows up in the automation tree,
    even though the controls around it do. Focusing or clicking it doesn't help, because there is no
    element to find. Upstream FlaUI notes the same Windows/.NET bug ([#74](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/74)). WPF spinners work
    normally.

    If you do find it, locate it by control type plus name: its automation id is not stable.

::: flaui.core.automation_elements.Spinner
