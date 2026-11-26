# Tree

!!! tip "Usage notes"
    - **Child items appear after their parent expands.** WPF creates a node's items only once the
      node is expanded, so reading `items` straight after `expand()` can return a partial list,
      especially on a slow CI machine. Wait for the children with `Retry.WhileEmpty` (or until the
      count you expect) before indexing into them ([#76](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/76)).
    - **Expand level by level.** Expand a parent, wait for its children, then go one level deeper.

::: flaui.core.automation_elements.Tree
