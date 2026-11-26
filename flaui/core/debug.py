"""Python wrapper for ``FlaUI.Core.Debug``: element dumps and XPath locators for debugging.

``FlaUI.Core.Debug`` is a static C# helper class with two methods:

- ``Debug.Details(element)`` returns a multi-line text dump of an element's identification
  properties, details, supported patterns and their values (and the same for its children).
- ``Debug.GetXPathToElement(element, rootElement)`` builds an XPath to the element from the
  desktop or from a given root.

Both are handy in failure messages and logs, and for turning an element you already found into a
locator you can paste back into :meth:`~flaui.core.automation_elements.AutomationElement.find_first_by_x_path`.
:class:`~flaui.core.automation_elements.AutomationElement` exposes the same calls as
:meth:`~flaui.core.automation_elements.AutomationElement.details` and
:meth:`~flaui.core.automation_elements.AutomationElement.get_xpath_to_element`.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from flaui.lib.exceptions import handle_csharp_exceptions

if TYPE_CHECKING:
    from flaui.core.automation_elements import ElementModel

logger = logging.getLogger(__name__)


@handle_csharp_exceptions
def details(element: ElementModel) -> str:
    """Return a multi-line text dump of an element's properties and supported patterns.

    Wraps ``FlaUI.Core.Debug.Details``. The text lists the identification properties (automation
    id, control type, name, help text, bounding rectangle, class name, offscreen state, framework
    id, process id) and the supported patterns, then the same block, indented, for each child.

    Like FlaUI C#, it does not raise when a property cannot be read: it returns an empty string.
    This happens intermittently on WinForms, whose MSAA proxy can reject the cached ``HelpText`` or
    ``AutomationId`` of an element or child. FlaUI reports the error with ``Console.WriteLine``,
    which itself fails when the process has no console (as under pytest's output capture), so the
    wrapper redirects the .NET console for the call and logs FlaUI's message as a warning on this
    module's logger instead.

    :param element: The element to describe (any wrapped automation element).
    :return: The details text, one ``Label: value`` per line; empty if FlaUI could not read it.
    """
    from FlaUI.Core import Debug as CSDebug
    from System import Console
    from System.IO import StringWriter

    captured = StringWriter()
    original_out = Console.Out
    Console.SetOut(captured)
    try:
        text = str(CSDebug.Details(element.raw_element))
    finally:
        Console.SetOut(original_out)
    message = str(captured.ToString()).strip()
    if message:
        logger.warning("FlaUI Debug.Details: %s", message)
    return text


@handle_csharp_exceptions
def get_xpath_to_element(element: ElementModel, root_element: Optional[ElementModel] = None) -> str:
    """Return an XPath to ``element``.

    Wraps ``FlaUI.Core.Debug.GetXPathToElement``. Each step is the element's control type, with a
    one-based ``[n]`` index when its parent has several children of that type, for example
    ``/Window[1]/Tab/TabItem[1]/RadioButton[1]``.

    - Without ``root_element`` the path starts at the desktop, so its first step is the top-level
      window.
    - With ``root_element`` the walk stops at the root **and leaves out the step for the root's
      direct child** (this matches FlaUI C#). Passing the desktop therefore returns a path relative
      to the top-level window, ready for ``window.find_first_by_x_path(path)``.

    :param element: The element to build the path to.
    :param root_element: An ancestor to stop at; the desktop when omitted. An element that is not
        an ancestor makes the walk run past the desktop, which raises on UIA3.
    :return: The XPath; an empty string when ``element`` is a direct child of ``root_element``.
    """
    from FlaUI.Core import Debug as CSDebug

    raw_root = None if root_element is None else root_element.raw_element
    return str(CSDebug.GetXPathToElement(element.raw_element, raw_root))
