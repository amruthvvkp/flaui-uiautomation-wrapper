# Robot Framework (planned post-v1)

!!! info "Planned for after v1.0"
    A first-class Robot Framework keyword library is **not part of the v1.0 scope** — it's tracked
    as post-v1 companion tooling alongside `pytest-flaui` and the recorder (see the
    [Roadmap](../roadmap.md) wishlist). You can already drive the
    wrapper from Robot Framework today using a thin custom library; the sketch below shows the
    shape such a library would take.

```text
*** Settings ***
Library    FlaUIRobotLibrary.py

*** Keywords ***
Open Notepad
    Setup Pythonnet Bridge
    Create Automation    UIA3
    Launch Application   notepad.exe
    Set Suite Variable    ${MAIN_WINDOW}

Click Save
    ${button}=    Find By AutomationId    ${MAIN_WINDOW}    123
    Invoke    ${button}
```

Notes:
- Library would wrap `Automation`, `Application`, and `ConditionFactory`.
- Provide keywords for launch/attach, find (id/name/xpath), invoke/click/type.
- Use `post_wait` where applicable for stability.
