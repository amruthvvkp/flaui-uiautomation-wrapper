# Event Handlers

Register UI Automation event handlers from Python. The ``register_*`` methods on
[`AutomationElement`](automation_element.md) and
[`AutomationBase`](automation_base.md) return an `EventRegistration` handle that keeps the callback
alive and can unregister it (also usable as a context manager).

```python
def on_invoked(element, event_id):
    print("invoked!")

registration = button.register_automation_event(
    button.patterns.invoke.pattern.raw_pattern.EventIds.InvokedEvent,
    TreeScope.Element,
    on_invoked,
)
# ... later ...
registration.unregister()
```

::: flaui.core.event_handlers.EventRegistration
