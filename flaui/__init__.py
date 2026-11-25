"""FlaUI for Python: the full FlaUI Windows UI Automation API, in Python.

The library logs through the ``flaui`` logger hierarchy (``flaui.lib.pythonnet_bridge``,
``flaui.core.application``, ...; C# messages arrive on ``flaui.csharp`` when enabled). A
:class:`logging.NullHandler` is attached here, so nothing is printed and your own logging setup is
left untouched until you configure logging yourself.
"""

import logging

logging.getLogger("flaui").addHandler(logging.NullHandler())
