# v1 code review audit (GH-85)

This is a read-only audit of `flaui/` against the conventions in `CLAUDE.md`. It covers the
"Code Review" items in [#85](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/issues/85):
consistency across modules, uniform naming, docstrings, unused code and complete type hints.

No library code was changed. Five PRs were editing the library while this audit ran (#157 to #161),
so the fixes are planned here and split into batches at the end. Apply them once those PRs merge.

- **Baseline:** `master` at `ac7496f`. Line numbers refer to that commit and will move once
  #157 to #161 merge, so look up the symbol name rather than trusting the line number.
- **Breaking?** One of three values:
    - **No:** callers see no change.
    - **Additive:** new names or parameters; the old ones keep working.
    - **Yes:** a public signature, return type or raised exception type changes. Ship these behind
      a deprecation alias, or call them out in the release notes.
- **Overlap:** the issue whose PR already touches the same code. Re-check those findings after that
  PR merges, because some will already be fixed.

| Issue | Scope | Files it touches |
|---|---|---|
| #157 | Missing `FlaUI.Core.Definitions` enums, converted at the boundary | `definitions.py`, `automation_elements.py`, event handlers |
| #158 | `and_`/`or_`/`not_` combinators and operators; true/false conditions | `condition_factory.py` |
| #159 | `FlaUI.Core.Debug` wrapper | new module; possibly `automation_elements.py` |
| #160 | Typed capture/video settings; overlay classes | `capturing.py`, `overlay.py` |
| #161 | Small parity gaps: `Menu`, `ProgressBar`, `CacheRequest.Add`, `PropertyId.GetCondition`, exception attributes, XPath navigator | `automation_elements.py`, `cache_request.py`, `lib/exceptions.py`, `xpath_navigator.py`, `identifiers/` |

## Tool results

All four tools were run on the baseline with `uv run --group dev`.

| Tool | Command | Result |
|---|---|---|
| interrogate | `interrogate flaui -v` | **PASSED**, 99.3% (1189/1197; gate is 95%). All 8 misses are `@overload` stubs in `automation_elements.py`: `Grid.select` (L1830, L1842), `Grid.add_to_selection` (L1883, L1895), `Grid.remove_from_selection` (L1939, L1944) and `Tab.select_tab_item` (L2765, L2777). See [D-1](#dead-code-and-lint-residue). |
| ty | `ty check flaui` | **All checks passed.** `[tool.ty.rules]` sets `import-not-found` and `missing-attribute` to `ignore`, so every C# value is typed as `Unknown`. A clean ty run says nothing about the interop boundary; that is what [section 5](#5-type-hints) covers. |
| vulture | `vulture` (whitelist included) | **Clean** (exit 0). Without the whitelist, `vulture flaui --min-confidence 60` reports 120 items, and almost all are public C#-parity API. The whitelist also hides three real issues: [D-3](#dead-code-and-lint-residue), [D-4](#dead-code-and-lint-residue) and [N-6](#1-naming). |
| pylint | `pylint flaui` | **9.91/10** (gate is 9.5), 44 messages, exit 28 (warning and refactor bits set). Breakdown: 7 × R1705 no-else-return, 6 × W0108 unnecessary-lambda, 6 × W0107 unnecessary-pass, 6 × W0105 pointless-string-statement, 4 × W0621 redefined-outer-name (`date`), 4 × W0603 global-statement, 4 × W0212 protected-access (`Mouse._apply_post_wait`, `CacheRequest._cs_instance`), 2 × W0622 redefined-builtin (`property`, `range`), 1 × W0201, 1 × W0106, 1 × R0912, 1 × C0103 (`cbSize`). |

## Correctness issues found during the review

These are behavior bugs rather than style issues. Fix them first.

| ID | Location | Finding | Suggested fix | Breaking? | Overlap |
|---|---|---|---|---|---|
| A-1 | `flaui/core/input.py:342` (`Mouse._apply_post_wait`) | `post_wait=True` waits **1 s**, not the documented 100 ms. `bool` is a subclass of `int`, so `isinstance(post_wait, (int, float))` matches `True` and calls `Wait.until_input_is_processed(1.0)`. The `# post_wait is True` branch below it can never run. This affects every `click(post_wait=True)` / `select_tab_item(..., post_wait=True)` in `tests/integration`. | Check `post_wait is True` before the numeric branch, or use `isinstance(post_wait, bool)`. Add a unit test that mocks `time.sleep`. | No (it makes the code match the docs) | — |
| A-2 | `CLAUDE.md` (`post_wait` section), `docs/contributing/testing.md:229` | Both say a float post-wait calls `Wait.for_seconds`. That method does not exist; the code calls `Wait.until_input_is_processed(seconds)`. | Fix both docs. | No | — |
| A-3 | `flaui/core/automation_elements.py:2789` (`Tab.select_tab_item`) | A `try/except Exception` swallows every failure and only logs it at `error`, so callers never learn that the tab was not selected. That defeats `@handle_csharp_exceptions`. It also calls `logging.getLogger(__name__)` inline rather than using a module logger. | Drop the `try/except` and let the decorator translate the error. Return the selected `TabItem`, as C# `SelectTabItem` does. Replace the conditional expression statement (pylint W0106) with an `if`. | Yes (it now raises; the return value is new) | #161 (file) |
| A-4 | `flaui/core/cache_request.py:71` (`CacheRequest.tree_scope`) | The getter is annotated `-> TreeScope` but returns the raw C# enum value. The setter, by contrast, expects a Python `TreeScope`. | `return TreeScope(int(self._cs_instance.TreeScope))`. Apply the same fix to `automation_element_mode` (L45) with `AutomationElementMode`. | Yes (return type) | #161 |
| A-5 | `flaui/core/automation_elements.py:3212` (`AutomationProperty.property_id`) | Annotated `-> str` but returns `PropertyId.Id`, which is an `int`. | Return the `PropertyId` wrapper (`flaui.core.identifiers.PropertyId(raw=...)`), or at least annotate it `-> int`. | Yes if it returns the wrapper; No if only the hint changes | #161 (PropertyId) |
| A-6 | `flaui/lib/system/drawing.py:221` (`ColorData`) | `ColorData` subclasses `pydantic_settings.BaseSettings` rather than `BaseModel`. That makes it read environment variables: a stray `CS_OBJECT` env var would be picked up as a field value. It is the only non-settings class that does this. | Change it to `BaseModel` with `model_config = ConfigDict(arbitrary_types_allowed=True)`, matching `Point`, `Size` and `Rectangle`. | No | — |
| A-7 | `flaui/lib/system/drawing.py:277-306` (`ColorData.a/r/g/b`) | Annotated `-> bytes`, but PythonNet converts C# `Byte` to `int`. | Annotate them `-> int`. | No | — |
| A-8 | `flaui/core/patterns/automation_pattern.py:35` (`AutomationPattern.pattern`) | The docstring says it raises `PatternNotSupportedException`, but there is no `@handle_csharp_exceptions`, so callers get the raw .NET exception. `is_supported` (L27) and `pattern_or_default` (L44) have the same problem. | Add the decorator to all three. | Yes (the raised exception type changes) | — |
| A-9 | `flaui/core/application.py:242` (`Application.get_main_window`) | `raise last_err` re-raises the raw C# exception from `GetMainWindow`. No `Application` member is decorated (see [E-1](#2-missing-handle_csharp_exceptions)). | Decorate it and raise a translated error. | Yes (exception type) | — |
| A-10 | `flaui/core/condition_factory.py:70` (`PropertyCondition.Or`) | The docstring says "Packs this condition into a not condition". | Fix the docstring, or let #158's `or_` replace it. | No | #158 |

## 1. Naming

These public names break the C# PascalCase → Python snake_case rule. Enum members and C#-facing
`KnownColor`/`ControlType` constants are exempt by design, as `[tool.pylint.basic]` notes.

| ID | Location | Names | Suggested fix | Breaking? | Overlap |
|---|---|---|---|---|---|
| N-1 | `flaui/core/condition_factory.py:37-106` | `PropertyCondition.And`, `Or`, `Not` | Add `and_`, `or_` and `not_`, and keep the PascalCase names as aliases. | Additive | **#158** |
| N-2 | `flaui/core/condition_factory.py:49-111` | `PropertyCondition.Equals`, `ToString`, `Property`, `PropertyConditionFlags`, `Value` | Add `equals()`, `to_string()`, `property`, `property_condition_flags` and `value`, matching `AutomationElement.to_string()` and `Point.equals()`. Keep the old names as deprecated aliases, then remove the remaining patterns from `good-names-rgxs`. | Additive | #158 (file; not in #158's stated scope) |
| N-3 | `flaui/core/tools.py:48-458` | `Retry.While`, `WhileNot`, `WhileTrue`, `WhileFalse`, `WhileNull`, `WhileNotNull`, `WhileEmpty`, `WhileException`, `IsTimeOutReached` | `while_` (since `while` is a keyword), `while_not`, `while_true`, `while_false`, `while_null`, `while_not_null`, `while_empty`, `while_exception` and `is_timeout_reached`. Keep the PascalCase names as aliases, and update docs/examples. `Retry` is pure Python, so nothing forces the C# casing. | Additive | — |
| N-4 | `flaui/lib/config.py:35-55` | `Settings.BIN_HOME`, `LOG_CSHARP`, `LOG_CSHARP_LEVEL`, `MAIN_WINDOW_TIMEOUT` | **Keep them.** Upper-case fields mirror the `FLAUI_*` environment variables, as pydantic-settings documents. Record the exemption in `CLAUDE.md` rule 9 so later reviews skip it. | No | — |
| N-5 | `flaui/core/input.py:54` | `Wait.until_responsive_hwnd(hWnd)` | Rename the parameter to `hwnd` and accept `hWnd` as a deprecated keyword for one release. | Yes (keyword name) | — |
| N-6 | `flaui/lib/system/drawing.py:1143` | `Rectangle.interset` is a typo of C# `Intersect`, and the vulture whitelist hides it as `_.interset`. | Add `intersect`, keep `interset` as a deprecated alias, and fix the whitelist entry. | Additive | — |
| N-7 | `flaui/core/application.py:269` | `launch_store_app(app_user_model_ltd)` is a typo of `app_user_model_id` (C# `appUserModelId`). | Rename it and accept the old keyword for one release. | Yes (keyword name) | — |
| N-8 | `flaui/core/automation_elements.py:820`, `flaui/core/text_range.py:54` | Parameters shadow builtins: `is_property_supported_direct(property)` and `TextRange.compare(range)` (pylint W0622). | Use `property_id` and `other`/`text_range`. | Yes (keyword name) | — |
| N-9 | `flaui/core/automation_elements.py:3221` (`AutomationProperty.to_string`) | This is a `@property`, but `to_string` is a method everywhere else (`AutomationElement.to_string()`, `Point.to_string()`, ...). | Make it a method. | Yes | — |
| N-10 | `flaui/core/automation_elements.py:3153` (`IAutomationProperty`) | The C#-style `I` interface prefix is the only one in the package; the other ABCs are named `ElementBase`, `PatternBase`, ... | Optional: rename it to `AutomationPropertyBase` and keep an alias. Low value. | Additive | — |

## 2. Missing `@handle_csharp_exceptions`

The scanner listed every public member whose body reads a PascalCase attribute on `self.*`, or calls
a name imported from `FlaUI`, `System` or `Interop`, and has no decorator. 221 hits, grouped below.
Adding the decorator changes what callers can catch: they get translated `flaui.lib.exceptions`
types instead of raw .NET exceptions. That is why these rows are marked **Yes**, even though
translated errors are the intended behavior.

| ID | Location | Members | Suggested fix | Breaking? | Overlap |
|---|---|---|---|---|---|
| E-1 | `flaui/core/application.py:104-318` | **All 19 members** of `Application`: `name`, `process_id`, `is_store_app`, `has_exited`, `main_window_handle`, `exit_code`, `close_timeout` (getter and setter), `get_all_top_level_windows`, `get_main_window`, `launch`, `launch_store_app`, `attach`, `attach_or_launch`, `kill`, `dispose`, `close`, `wait_while_main_handle_is_missing`, `wait_while_busy` | Decorate each one. The retry loops in `get_main_window` and `launch` catch broadly on purpose; keep that, but translate the final raise. | Yes (exception type) | — |
| E-2 | `flaui/core/input.py:38-770` | `Wait.until_responsive`, `until_responsive_hwnd`; all 12 `Keyboard` methods; `PressedKeys.release`; `Mouse.are_buttons_swapped` and all 15 `Mouse` actions; `Interpolation.execute`, `execute_single`, `execute_rotation`; all 6 `Touch` methods | Add the decorator below `@staticmethod`. | Yes (exception type) | — |
| E-3 | `flaui/core/patterns/patterns.py:69-392` | All 34 `Patterns.<pattern>` properties | Decorate them. Each one reads `self.raw_patterns.<X>`, which can raise if the element has gone stale. | Yes (exception type) | — |
| E-4 | `flaui/core/patterns/automation_pattern.py:27-50` | `is_supported`, `pattern`, `pattern_or_default` | See A-8. | Yes | — |
| E-5 | `flaui/core/condition_factory.py:37-290` | All `PropertyCondition` members and all 15 `ConditionFactory.by_*`/`menu`/`grid`/`*_scroll_bar` builders | Decorate them. #158's "Done when" already requires this for the new combinators, so extend it to the whole file. | Yes (exception type) | **#158** |
| E-6 | `flaui/core/cache_request.py:26-141` | All 16 members, including the `@classmethod`s `is_caching_active`, `current`, `push`, `pop`, `force_no_cache` | Decorate them. | Yes (exception type) | **#161** |
| E-7 | `flaui/core/identifiers/identifier_base.py:36,44`, `identifiers/pattern_id.py:13` | `IdentifierBase.id`, `name`, `PatternId.availability_property` | Decorate them. | Yes (exception type) | #161 (PropertyId) |
| E-8 | `flaui/core/tools.py:476-536` | `ItemRealizer.realize_items`, `AccessibilityTextResolver.get_role_text`, `get_state_bit_text`, `get_state_text`, `WindowsStoreAppLauncher.launch` | Decorate them. | Yes (exception type) | — |
| E-9 | `flaui/core/xpath_navigator.py:30` | `AutomationElementXPathNavigator.from_element` | Decorate it. | Yes (exception type) | **#161** |
| E-10 | `flaui/core/capturing.py:42,218` | `CaptureSettings.cs_object`, `VideoRecorderSettings.cs_object` | Fold this into #160's typed settings models. | — | **#160** |
| E-11 | `flaui/lib/collections.py:32,44` | `TypeCast.cs_timespan`, `cs_datetime` | Decorate them, or leave them: they are pure conversions and only fail on bad input. Low value. | No | — |
| E-12 | `flaui/lib/system/drawing.py` (70 members) | Every `ColorData`, `Point`, `Size` and `Rectangle` property and method | **Don't decorate them.** These are `System.Drawing` value-type operations that cannot raise UIA errors, and the decorator would cost a call on every coordinate read. Add an explicit exemption to `CLAUDE.md` coding standard 3 ("value-type wrappers in `lib/system/drawing.py` are exempt") so the rule and the code agree. | No | — |
| E-13 | `flaui/core/logging.py:50,86`, `flaui/lib/pythonnet_bridge.py:16` | `enable_csharp_logging`, `disable_csharp_logging`, `setup_pythonnet_bridge` | Leave them. These are bootstrap helpers that log on purpose rather than raise, and the bridge runs before the exception types can be imported. Note the exemption in `CLAUDE.md`. | No | — |

## 3. Raw C# values returned without conversion

| ID | Location | Member → returns | Suggested fix | Breaking? | Overlap |
|---|---|---|---|---|---|
| R-1 | `flaui/core/automation_elements.py:778-799` | `get_supported_patterns`, `get_supported_patterns_direct` → lists of raw C# `PatternId`; `get_supported_properties_direct` → raw `PropertyId` | Wrap each item in the existing `flaui.core.identifiers.PatternId` / `PropertyId`, and annotate them `List[PatternId]` / `List[PropertyId]`. | Yes (element type) | #161 (identifiers) |
| R-2 | `flaui/core/automation_elements.py:802-826, 760`; `patterns/item_container_pattern.py:18` | `is_pattern_supported(pattern_id: Any)`, `is_pattern_supported_direct`, `is_property_supported_direct`, `get_current_metadata_value(property_id: Any)`, `find_item_by_property(property_id: Any)` accept only raw ids. | Accept the wrapper or the raw id via `coerce_property_id`/`getattr(x, "raw", x)`, as the event APIs already do, and annotate them `Union[PatternId, Any]`. | Additive | #161 |
| R-3 | `flaui/core/automation_elements.py:860-1025` (event registration) | The callbacks pass raw C# `EventId`, `PropertyId`, `StructureChangeType`, `NotificationKind`/`NotificationProcessing` and `TextEditChangeType` values to user code. | Wrap the ids in `EventId`/`PropertyId`, and the enums once #157 adds them. | Yes (callback argument types) | **#157** (enums) |
| R-4 | `flaui/core/automation_elements.py:152,161` | `ElementBase.cached_children -> Any` (a raw C# array), `cached_parent -> Any` (a raw element). `Grid.cached_children` (L2070) already returns `List[GridCell]`. | Return `List[AutomationElement]` / `Optional[AutomationElement]`. | Yes | — |
| R-5 | `flaui/core/automation_elements.py:1459` | `ComboBox.animation_duration -> Any` returns a raw `TimeSpan`, while its setter takes `int` milliseconds. | Return `int` milliseconds (`TotalMilliseconds`) to match the setter. | Yes | — |
| R-6 | `flaui/core/automation_base.py:101-143` | `transaction_timeout` and `connection_timeout` return and accept a raw `TimeSpan`; `connection_recovery_behavior` and `coalesce_events` return a raw C# enum. | Convert the timeouts to `int` ms (or `timedelta`) using `TypeCast.cs_timespan` on the way in. Convert the two enums to `ConnectionRecoveryBehaviorOptions` / `CoalesceEventsOptions` once #157 adds them. | Yes | **#157** (enums) |
| R-7 | `flaui/core/automation_base.py:39-97` | `property_library`, `event_library`, `pattern_library`, `text_attribute_library`, `tree_walker_factory`, `not_supported_value`, `mixed_attribute_value` → raw C# | Acceptable as interop escape hatches for now. Document them as raw, and annotate them `Any` with a "raw C#" note. A typed `TreeWalker` wrapper is a post-v1 item. | No | — |
| R-8 | `flaui/modules/automation.py:49` | `Automation.tree_walker` is a raw C# `ITreeWalker`. | Same as R-7: document it as raw for v1, and wrap it post-v1. | No | — |
| R-9 | `flaui/core/automation_elements.py:3266` (`AutomationProperty.try_get_value`) | Returns PythonNet's raw `(bool, value)` out-parameter tuple, without `cast_to_py_wrapper`, and is annotated `Tuple[bool, str]`. | Return `(ok, self.cast_to_py_wrapper(value))` and annotate it `Tuple[bool, Any]`. | Yes (value type) | #157 (enum values via `cast_to_py_wrapper`) |
| R-10 | `flaui/core/automation_elements.py:3230` (`AutomationProperty.cast_to_py_wrapper`) | Converts `Color`/`Point`/`Size`/`Rectangle` but not C# enums or `AutomationElement`, so `value` on `HeadingLevel`, `LandmarkType` and similar properties stays raw. | Extend it once #157 lands. | Yes | **#157** |
| R-11 | `flaui/core/automation_elements.py:478` (`AutomationElement.capture`) | Returns a raw `System.Drawing.Bitmap`, while `Capture.element()` returns the `CaptureImage` wrapper. | Keep the C# return type for parity, but annotate and document it as raw `Bitmap`, and point callers to `Capture.element()`. | No | #160 |
| R-12 | `flaui/core/capturing.py:71` (`CaptureImage.bitmap`) | A raw `Bitmap`. | Same as R-11. | No | **#160** |
| R-13 | `flaui/core/text_range.py:113`, `patterns/object_model_pattern.py:15` | `TextRange.get_attribute_value` → raw value; `get_underlying_object_model` → raw COM object | `get_attribute_value`: run it through `cast_to_py_wrapper` and the #157 enums. The object model is inherently raw; document it. | Yes / No | #157 |
| R-14 | `flaui/core/cache_request.py:45-139` | `automation_element_mode`, `tree_filter`, `patterns`, `properties`, `force_no_cache` → raw C# | Convert to enums/`PropertyCondition`/lists of identifier wrappers. `force_no_cache` should be a context manager, like `activate`. | Yes | **#161** |

## 4. Inconsistent patterns across modules

| ID | Topic | Finding | Suggested fix | Breaking? | Overlap |
|---|---|---|---|---|---|
| P-1 | Pydantic vs plain classes | Most wrappers are Pydantic models, but `Application` (`application.py:64`), `CacheRequest` (`cache_request.py:21`), `PressedKeys` (`input.py:240`) and `Automation` (`modules/automation.py:15`) are plain classes. Each holds its C# object differently: `_application` (a class attribute that starts out as the C# **type**), `_cs_instance` and `_cs_disposable`. | For v1, at least name the holders consistently: `raw_application`, `raw_cache_request`, `raw_disposable`. Moving `Application`/`CacheRequest` to Pydantic is optional; `Automation` and the static helper classes (`Wait`, `Keyboard`, `Mouse`, `Touch`, `Retry`, `Capture`) can stay plain. | No if private names only | #161 (`CacheRequest`) |
| P-2 | Holder field names | The fields that hold C# objects are named `raw_element`, `raw_pattern`, `raw_patterns`, `raw_automation_pattern`, `raw_automation`, `raw_text_range`, `raw_navigator`, `raw_overlay_manager`, `raw_image`, `raw_recorder`, `raw_property`, `raw_properties`, `raw_cf`, `raw` (identifiers), `raw_value` (drawing), `cs_condition`, and `cs_object`. `cs_object` is a **field** on `ColorData` but a **property** on `Point`/`Rectangle`/`CaptureSettings`. | Document the convention: `raw_<thing>` is the stored C# reference, and `cs_object` is a computed "give me the C# value" property. For v1, rename only the outliers, via aliases: `ColorData.cs_object` → `raw_value`, and `ConditionFactory.raw_cf` → `raw_condition_factory`. `cs_condition` is part of the documented API, so keep it. | Additive | #158 (`cs_condition`) |
| P-3 | `model_config` | `ElementModel` (`automation_elements.py:54`), `IAutomationProperty` (L3153), `Properties` (L3291), `CaptureSettings` and `VideoRecorderSettings` have no `model_config`, while every other wrapper sets `arbitrary_types_allowed=True`. It works today only because their fields are `Any`. | Add `model_config = ConfigDict(arbitrary_types_allowed=True)` to the base classes so subclasses can use real C# types in their annotations. | No | #160 (settings) |
| P-4 | Constructors | `CacheRequest(_cs_instance=...)` has a public constructor parameter with a leading underscore, and it silently ignores an `Automation` argument (L36-39). `Application()` starts out holding the C# **class**, and `launch`/`attach` mutate `self` and return `None`, whereas C# `Application.Launch` is a static factory. | `CacheRequest(raw_cache_request=None)`, and drop the `Automation` branch or raise on it. For `Application`, add `@classmethod` factories `Application.launch_new(...)` / `attach_to(...)` that return an instance, and keep the mutating methods for compatibility. | Additive | #161 (`CacheRequest`) |
| P-5 | `post_wait` coverage | `AutomationElement.click`, `Tab.select_tab_item`, `TextBox.enter` and every `Mouse` method take `post_wait`. `AutomationElement.double_click` (L509), `right_click` (L1029), `right_double_click` (L1037), all `Keyboard` methods and `Touch` do not. | Add `post_wait` to the three element click variants. For `Keyboard`, either add it or say in `CLAUDE.md` that it is mouse/element-only. | Additive | — |
| P-6 | `post_wait` type | `Optional[Union[bool, float, Callable[[], None]]]` is spelled out 21 times, and every caller reaches into the private `Mouse._apply_post_wait` (pylint W0212 ×3). | Add a `PostWait` type alias and a public `apply_post_wait()` function in `flaui/core/input.py`; keep `Mouse._apply_post_wait` as a shim. | No | — |
| P-7 | Timeout units | `Retry.*`, `Application.wait_*` (`time_out`), `Automation(timeout=)`, `expectations` and `TypeCast.cs_timespan` use **milliseconds**. `Wait.until_input_is_processed`, `until_responsive` (`timeout_in_secs`), `until_responsive_hwnd` (`timeout`, but in seconds) and `while_cursor_is_busy` use **seconds**. The parameter is variously called `timeout`, `time_out`, `timeout_in_secs` and `wait_timeout_in_secs`. | Decide on milliseconds for v1 (matching C# `TimeSpan.FromMilliseconds` usage and the larger share of the API) and record it in `CLAUDE.md`. Rename `time_out` → `timeout`, and give the seconds-based `Wait` helpers a `_secs` suffix consistently (`until_responsive_hwnd(timeout=)` is the outlier). | Yes (keyword names) | — |
| P-8 | Logging | Every module uses `logging.getLogger(__name__)` at module level except: `automation_elements.py:2809` (an inline `logging.getLogger(__name__)` inside `Tab.select_tab_item`; see A-3) and `core/logging.py:96,113` (inline `getLogger(__name__)` twice). No module calls `logging.info()` directly. | Add a module-level `logger` to both files. | No | — |
| P-9 | Late imports | They follow `CLAUDE.md`. The only top-level C# import in `automation_elements.py` is `System.NullReferenceException` (L16). `cache_request.py:16` imports `flaui.modules.automation` at module level just for the `isinstance` in P-4, which pulls the high-level module into a core one. | Drop that import along with the P-4 fix. | No | #161 |
| P-10 | Return type of `to_string` / `__eq__` | `AutomationProperty.__eq__` (L3274) is defined without a `__hash__`, which makes instances unhashable, and it carries `@handle_csharp_exceptions` on a dunder method. | Add `__hash__ = None` explicitly, or hash by `property_id`. | No | — |
| P-11 | Return of mutating calls | `Application.launch`/`attach`/`attach_or_launch` return `None`; C# returns the `Application`. | Return `self` so calls can chain. | Additive | — |

## 5. Type hints

### Missing annotations

All of these are in `flaui/core/automation_elements.py`. All are additive and non-breaking.

| ID | Location | Member | Fix |
|---|---|---|---|
| H-1 | L2523, L2528, L2533, L2538 | `Slider.small_increment`, `small_decrement`, `large_increment`, `large_decrement` | `-> None` |
| H-2 | L2618, L2623 | `Spinner.increment`, `decrement` | `-> None` |
| H-3 | L2849 | `TextBox.enter` | `-> None` |
| H-4 | L2865, L2873 | `Thumb.slide_horizontally`, `slide_vertically` | `-> None` |
| H-5 | L2925 | `ToggleButton.toggle` | `-> None` |
| H-6 | L2994, L2999, L3004 | `TreeItem.expand`, `collapse`, `select` | `-> None` |
| H-7 | L3131, L3136, L3145 | `Window.close`, `move`, `set_transparency` | `-> None` |
| H-8 | L3230 | `AutomationProperty.cast_to_py_wrapper(value)` | `(value: Any) -> Any` |
| H-9 | L3274, L3286 | `AutomationProperty.__eq__(other)`, `__str__` | `(other: object) -> bool`, `-> str` |

### `Any` where a real type is known

The scan found 133 `Any` annotations. Holders of raw C# objects (`raw_*: Any`) and validator
signatures are correct as `Any` and are left out. These are the ones that matter:

| ID | Location | Now | Should be | Breaking? | Overlap |
|---|---|---|---|---|---|
| T-1 | `patterns/text_child_pattern.py:17`, `patterns/spreadsheet_pattern.py:15`, `text_range.py:140` | `text_container -> Any`, `get_item_by_name -> Any`, `get_enclosing_element -> Any`; each already returns `AutomationElement` | `-> "AutomationElement"` (import under `TYPE_CHECKING`) | No | — |
| T-2 | `text_range.py:130` | `get_children -> List[Any]` | `-> List["AutomationElement"]` | No | — |
| T-3 | `automation_elements.py:778-799` | `get_supported_* -> Any` (returns a list) | `List[PatternId]` / `List[PropertyId]` (see R-1) | No (hint only) | #161 |
| T-4 | `automation_base.py:188` | `register_focus_changed_event(action: Any) -> Any` | `(action: Callable[["AutomationElement"], None]) -> "EventRegistration"`, matching the element-level registrations | No | — |
| T-5 | `automation_base.py:229` | `compare(element1: Any, element2: Any)` | `Union["AutomationElement", Any]` (it accepts wrappers or raw values) | No | — |
| T-6 | `application.py:169,178` | `get_all_top_level_windows(automation: Any)`, `get_main_window(automation: Any)` | `Union[AutomationBase, "Automation", Any]`, mirroring `_coerce_cs_automation` | No | — |
| T-7 | `automation_elements.py:724` | `find_first_with_options(root: Any)` | `Optional["AutomationElement"]` | No | — |
| T-8 | `automation_elements.py:993` | `register_text_edit_text_changed_event_handler(text_edit_change_type: Any)` | `TextEditChangeType` | No | **#157** |
| T-9 | `core/event_handlers.py:99-233` | `coerce_*` and `make_*_delegate -> Any` | These are internal helpers; leave them as `Any` or make them private (`_coerce_*`). | No | — |
| T-10 | `lib/collections.py:32` | `cs_timespan(value: int) -> Any`; it also accepts `None` | `(value: Optional[int]) -> Optional[TimeSpan]` | No | — |
| T-11 | `core/expectations.py:158` | `to_have_value(expected: Any)` | Fine as-is (any comparable value). | — | — |
| T-12 | `core/input.py:591-672` | `Interpolation.execute*(action: Any)` | `Callable[[Point], None]` / `Callable[[List[Point]], None]` | No | — |
| T-13 | `core/tools.py:495-517` | `AccessibilityTextResolver.get_role_text(role: Any)`, `get_state_*_text(state: Any)` | `AccessibilityRole` / `AccessibilityState` (already in `windows_api.py:915` / `:880`), accepting the raw `int` as well | No | — |
| T-14 | `core/capturing.py:42,71,90,218` | `cs_object -> Any`, `apply_overlays(*overlays: Any)` | The #160 overlay classes | No | **#160** |
| T-15 | `core/logging.py:50` | `enable_csharp_logging -> Any` | Annotate the actual sink handle type, or `None`. | No | — |
| T-16 | `automation_base.py:107-143` | `value: Any` on the TimeSpan/enum setters | See R-6. | Yes | #157 |

## Dead code and lint residue

| ID | Location | Finding | Suggested fix | Breaking? | Overlap |
|---|---|---|---|---|---|
| D-1 | `automation_elements.py:1830-1944, 2765-2781` | The `@overload` stubs carry their docs as bare string statements **after** the `def ...: ...` line. pylint reports them as W0105 (×6) and interrogate counts them as missing docstrings (all 8 of its misses). | Make them real docstrings inside the stubs. That clears both tools. | No | — |
| D-2 | `automation_elements.py:1375, 2815, 3161-3184` | `pass` after a docstring (W0107 ×6); unnecessary `lambda h: ...` wrappers in the event registrations (L856-1025, W0108 ×6); `else`/`elif` after `return` (R1705 ×7). | Mechanical cleanup. | No | — |
| D-3 | `flaui/lib/config.py:69` (`VideoRecordingMode`) | It has no consumer in the package. The whitelist keeps it "for API stability", and only `tests/` references it. It also has a `NONE = None` member. | Remove it, or wire it into the #160 video settings. Remove the whitelist entries (`VideoRecordingMode`, `ONEPERTEST`, `ONEPERFIXTURE`). | Yes if removed (it is importable) | **#160** |
| D-4 | `flaui/modules/automation.py:42` (`Automation._ui_automation_types`) | It is written and never read; the whitelist hides it. The class docstring documents a public `ui_automation_type` attribute that does not exist. | Add a read-only `ui_automation_type` property backed by `_ui_automation_type` (singular), and drop the whitelist entry. | Additive | — |
| D-5 | `vulture_whitelist.py` | After D-3, D-4 and N-6, prune the matching entries. Everything else in the whitelist was checked: each name is either public C#-parity API used by tests/docs, or a PythonNet/protocol hook (`OnLog`, `IsBackground`, `cbSize`, `keep_alive`, `_callback`, `exc_info`/`obj`/`objtype`). | — | No | — |
| D-6 | `automation_elements.py:1392,1412,1710`, `lib/collections.py:44` | Parameters named `date` shadow the imported `datetime.date` (W0621 ×4). | Rename them to `value`/`date_value`, keeping keyword compatibility where they are public. | Yes for public keyword names | — |
| D-7 | `lib/exceptions.py:247` (`_raise_translated`) | Too many branches (R0912, 13/12). | Replace the `if` chain with a type→exception lookup table. | No | #161 (`lib/exceptions.py`) |
| D-8 | `core/logging.py:81,90`, `lib/pythonnet_bridge.py:27`, `lib/threading_utils.py:120` | `global` statements (W0603 ×4) for module singletons. | Acceptable; disable W0603 inline with a reason, or keep it as is. | No | — |

## Proposed PR batches (after #157 to #161 merge)

Each batch can be reviewed on its own and runs green on the existing gates. Batches 1 to 3 are
non-breaking and can ship in any 1.0 pre-release. Batches 4 and 5 change public types or names, so
they should land before 1.0 final with deprecation aliases where marked.

1. **`fix: post_wait, swallowed errors and wrong hints` (bugs)**: A-1, A-2, A-3, A-5 (hint only),
   A-6, A-7, A-10, D-1, H-1 to H-9. Small diff, high value. A-1 needs a unit test that mocks
   `time.sleep`. *Files:* `input.py`, `automation_elements.py`, `drawing.py`, `CLAUDE.md`,
   `docs/contributing/testing.md`.
2. **`refactor: translate C# exceptions everywhere`**: A-8, A-9, E-1 to E-9, E-11, plus the
   `CLAUDE.md` exemptions for E-12/E-13. This changes the exception types callers see, from raw
   .NET to `flaui.lib.exceptions`, so add a changelog note. Split it into two PRs if the diff is
   large: (a) `application.py` and `input.py`; (b) `patterns/`, `identifiers/`, `cache_request.py`,
   `condition_factory.py`, `tools.py`, `xpath_navigator.py`. Rebase after #158 and #161, which
   edit `condition_factory.py`, `cache_request.py` and `xpath_navigator.py`.
3. **`chore: type hints and lint residue`**: T-1, T-2, T-4 to T-7, T-9, T-10, T-12, T-15, D-2,
   D-4, D-5, D-8, P-6 (`PostWait` alias and public `apply_post_wait`), P-8, P-10. Hints only, no
   runtime change. It should keep ty, pylint (the score rises) and vulture green.
4. **`feat!: convert identifiers, enums and TimeSpans at the boundary`**: A-4, A-5 (wrapper),
   R-1 to R-6, R-9, R-10, R-13, R-14, T-3, T-8, T-13, T-16. This depends on #157 (enums) and #161
   (`PropertyId.GetCondition`, `CacheRequest.Add`). Return types change, so list each change in
   the release notes.
5. **`refactor!: snake_case and consistent signatures`**: N-2, N-3, N-5 to N-9, P-1, P-2, P-4,
   P-5, P-7, P-11, D-3, D-6, D-7. Each rename keeps a deprecated alias (via a small
   `_deprecated_alias` helper that emits `DeprecationWarning`) for one minor release. N-1 is
   already handled by #158. The rest of #158's file (N-2) is the part left over.

Out of scope for v1, worth a tracking issue: a typed `TreeWalker` wrapper (R-7/R-8), and a
`Bitmap`→PIL convenience for `capture()`/`CaptureImage.bitmap` (R-11/R-12).
