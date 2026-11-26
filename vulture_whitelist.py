"""Vulture whitelist for the public API of the ``flaui`` package.

``flaui`` is a library: most of its public classes, methods and attributes are never called from
inside the package itself, only by users and by ``tests/``. Vulture is configured in
``[tool.vulture]`` (``pyproject.toml``) to skip anything decorated with ``@property``,
``@handle_csharp_exceptions``, ``@staticmethod`` / ``@classmethod`` and Pydantic validators, which
covers most of the C#-parity surface. The names below are the remaining intentionally-"unused"
public API and interop hooks, grouped by module.

Regenerate a draft with::

    uv run --group dev vulture flaui --make-whitelist

then review it: only add names that are genuinely public API or required by PythonNet / a Python
protocol. Real dead code should be deleted instead of whitelisted.
"""

# ruff: noqa: F821, B018

# --- flaui/core/application.py -----------------------------------------------------------------------
# Public API (C# parity), used by callers and tests rather than inside the package.
_.get_all_top_level_windows  # unused method
_.get_main_window  # unused method
_.launch  # unused method
_.launch_store_app  # unused method
_.attach  # unused method
_.kill  # unused method
_.wait_while_busy  # unused method

# --- flaui/core/automation_elements.py ---------------------------------------------------------------
# Public API (C# parity), used by callers and tests rather than inside the package.
_.where  # unused method
_.select  # unused method
_.add_to_selection  # unused method
_.remove_from_selection  # unused method
_.select_tab_item  # unused method

# --- flaui/core/cache_request.py ---------------------------------------------------------------------
# Public API (C# parity), used by callers and tests rather than inside the package.
_.add_pattern  # unused method
_.add_property  # unused method
_.activate  # unused method

# --- flaui/core/capturing.py -------------------------------------------------------------------------
# C# `CaptureSettings` / `VideoRecorderSettings` properties assigned for PythonNet, the `VideoFormat.xvid`
# enum member, `__exit__` protocol parameters, and `keep_alive` (holds the C# delegate so it is not GC'd).
xvid  # unused variable
_.OutputWidth  # unused attribute
_.OutputHeight  # unused attribute
_.OutputScale  # unused attribute
exc_info  # unused variable
_.ffmpegPath  # unused attribute
_.FrameRate  # unused attribute
_.UseCompressedImages  # unused attribute
_.VideoQuality  # unused attribute
_.EncodeWithLowPriority  # unused attribute
_.LogMissingFrames  # unused attribute
keep_alive  # unused variable

# --- flaui/core/condition_factory.py -----------------------------------------------------------------
# Public API (C# parity), used by callers and tests rather than inside the package.
_.by_automation_id  # unused method
_.by_control_type  # unused method
_.by_class_name  # unused method
_.by_name  # unused method
_.by_text  # unused method
_.by_framework_id  # unused method
_.by_framework_type  # unused method
_.by_process_id  # unused method
_.by_localized_control_type  # unused method
_.by_help_text  # unused method
_.by_value  # unused method
_.menu  # unused method
_.grid  # unused method
_.horizontal_scroll_bar  # unused method
_.vertical_scroll_bar  # unused method

# --- flaui/core/event_handlers.py --------------------------------------------------------------------
# `_callback` keeps the Python callback alive for as long as the C# handler is registered.
_._callback  # unused attribute

# --- flaui/core/expectations.py ----------------------------------------------------------------------
# Public API (C# parity), used by callers and tests rather than inside the package.
_.to_be_visible  # unused method
_.to_be_enabled  # unused method
_.to_be_offscreen  # unused method
_.to_be_checked  # unused method
_.to_have_name  # unused method
_.to_have_text  # unused method
_.to_have_value  # unused method
expect  # unused function

# --- flaui/core/input.py -----------------------------------------------------------------------------
# Descriptor / context-manager protocol parameters (`obj`, `objtype`, `exc_info`), C#-backed class-level
# Mouse settings exposed through the `_MouseMeta` descriptors, and the ctypes `CURSORINFO.cbSize` field.
_.cbSize  # unused attribute
exc_info  # unused variable
obj  # unused variable
objtype  # unused variable
move_pixels_per_millisecond  # unused variable
move_pixels_per_step  # unused variable
position  # unused variable

# --- flaui/core/logging.py ---------------------------------------------------------------------------
# C# `EventLogger.OnLog` event subscribed / unsubscribed with `+=` / `-=`.
_.OnLog  # unused attribute

# --- flaui/core/patterns/automation_pattern.py -------------------------------------------------------
# Public API (C# parity), used by callers and tests rather than inside the package.
_.try_get_pattern  # unused method

# --- flaui/core/tools.py -----------------------------------------------------------------------------
# Public API (C# parity), used by callers and tests rather than inside the package.
SystemInfo  # unused class

# --- flaui/lib/config.py -----------------------------------------------------------------------------
# `VideoRecordingMode` enum kept for API stability (see follow-ups in the GH-85 static-analysis PR).
VideoRecordingMode  # unused class
ONEPERTEST  # unused variable
ONEPERFIXTURE  # unused variable

# --- flaui/lib/enums.py ------------------------------------------------------------------------------
# `KnownClassNames` member mirroring the C# class-name constant.
TabControl  # unused variable

# --- flaui/lib/exceptions.py -------------------------------------------------------------------------
# Public API (C# parity), used by callers and tests rather than inside the package.
translate_exceptions  # unused function

# --- flaui/lib/pythonnet_bridge.py -------------------------------------------------------------------
# Public bootstrap entry point, called by users and `tests/conftest.py`.
setup_pythonnet_bridge  # unused function

# --- flaui/lib/system/drawing.py ---------------------------------------------------------------------
# Public API (C# parity), used by callers and tests rather than inside the package.
_.equals  # unused method
_.get_brightness  # unused method
_.get_hash_code  # unused method
_.get_hue  # unused method
_.get_saturation  # unused method
_.to_argb  # unused method
_.to_known_color  # unused method
_.to_string  # unused method
_.offset  # unused method
_.subtract  # unused method
_.to_size  # unused method
_.to_point  # unused method
_.contains  # unused method
_.from_ltrb  # unused method
_.inflate  # unused method
_.interset  # unused method
_.intersects_with  # unused method
_.union  # unused method
_.immediate_exterior_north  # unused method
_.immediate_interior_north  # unused method
_.immediate_exterior_east  # unused method
_.immediate_interior_east  # unused method
_.immediate_exterior_south  # unused method
_.immediate_interior_south  # unused method
_.immediate_exterior_west  # unused method
_.immediate_interior_west  # unused method
_.make_even  # unused method

# --- flaui/lib/threading_utils.py --------------------------------------------------------------------
# C# `Thread.IsBackground` set on the STA worker, and the public `get_sta_executor` helper.
_.IsBackground  # unused attribute
get_sta_executor  # unused function

# --- flaui/modules/automation.py ---------------------------------------------------------------------
_.cf  # unused attribute
_.tree_walker  # unused attribute
