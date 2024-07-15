"""Wrapper for Enums listed in FlaUI.Core.WindowsAPI namespace"""

from enum import Enum

from FlaUI.Core.WindowsAPI import (  # pyright: ignore
    AccessibilityRole as CSAccessibilityRole,
    AccessibilityState as CSAccessibilityState,
    AllocationType as CSAllocationType,
    CommonHresultValues as CSCommonHresultValues,
    CursorState as CSCursorState,
    InjectedInputVisualizationMode as CSInjectedInputVisualizationMode,
    InputType as CSInputType,
    KeyEventFlags as CSKeyEventFlags,
    LayeredWindowAttributes as CSLayeredWindowAttributes,
    MemoryProtection as CSMemoryProtection,
    MouseEventDataXButtons as CSMouseEventDataXButtons,
    MouseEventFlags as CSMouseEventFlags,
    PointerButtonChangeType as CSPointerButtonChangeType,
    PointerFlags as CSPointerFlags,
    PointerInputType as CSPointerInputType,
    ProcessAccessFlags as CSProcessAccessFlags,
    ScanCodeShort as CSScanCodeShort,
    SendMessageTimeoutFlags as CSSendMessageTimeoutFlags,
    SetWindowPosFlags as CSSetWindowPosFlags,
    ShowWindowTypes as CSShowWindowTypes,
    StretchMode as CSStretchMode,
    SystemMetric as CSSystemMetric,
    TernaryRasterOperations as CSTernaryRasterOperations,
    TouchFlags as CSTouchFlags,
    TouchMask as CSTouchMask,
    VirtualKeyShort as CSVirtualKeyShort,
    VkKeyScanModifiers as CSVkKeyScanModifiers,
    WindowLongParam as CSWindowLongParam,
    WindowsMessages as CSWindowsMessages,
    WindowStyles as CSWindowStyles,
)


class CommonHresultValues(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.CommonHresultValues enum"""

    # TODO: Add inline description
    E_ABORT = CSCommonHresultValues.E_ABORT
    E_ACCESSDENIED = CSCommonHresultValues.E_ACCESSDENIED
    E_FAIL = CSCommonHresultValues.E_FAIL
    E_HANDLE = CSCommonHresultValues.E_HANDLE
    E_INVALIDARG = CSCommonHresultValues.E_INVALIDARG
    E_NOINTERFACE = CSCommonHresultValues.E_NOINTERFACE
    E_NOTIMPL = CSCommonHresultValues.E_NOTIMPL
    E_OUTOFMEMORY = CSCommonHresultValues.E_OUTOFMEMORY
    E_POINTER = CSCommonHresultValues.E_POINTER
    E_UNEXPECTED = CSCommonHresultValues.E_UNEXPECTED
    S_OK = CSCommonHresultValues.S_OK


class WindowsMessages(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.WindowsMessages enum"""

    # TODO: Add inline description
    WM_ACTIVATE = CSWindowsMessages.WM_ACTIVATE
    WM_ACTIVATEAPP = CSWindowsMessages.WM_ACTIVATEAPP
    WM_AFXFIRST = CSWindowsMessages.WM_AFXFIRST
    WM_AFXLAST = CSWindowsMessages.WM_AFXLAST
    WM_APP = CSWindowsMessages.WM_APP
    WM_APPCOMMAND = CSWindowsMessages.WM_APPCOMMAND
    WM_ASKCBFORMATNAME = CSWindowsMessages.WM_ASKCBFORMATNAME
    WM_CANCELJOURNAL = CSWindowsMessages.WM_CANCELJOURNAL
    WM_CANCELMODE = CSWindowsMessages.WM_CANCELMODE
    WM_CAPTURECHANGED = CSWindowsMessages.WM_CAPTURECHANGED
    WM_CHANGECBCHAIN = CSWindowsMessages.WM_CHANGECBCHAIN
    WM_CHANGEUISTATE = CSWindowsMessages.WM_CHANGEUISTATE
    WM_CHAR = CSWindowsMessages.WM_CHAR
    WM_CHARTOITEM = CSWindowsMessages.WM_CHARTOITEM
    WM_CHILDACTIVATE = CSWindowsMessages.WM_CHILDACTIVATE
    WM_CLEAR = CSWindowsMessages.WM_CLEAR
    WM_CLOSE = CSWindowsMessages.WM_CLOSE
    WM_COMMAND = CSWindowsMessages.WM_COMMAND
    WM_COMMNOTIFY = CSWindowsMessages.WM_COMMNOTIFY
    WM_COMPACTING = CSWindowsMessages.WM_COMPACTING
    WM_COMPAREITEM = CSWindowsMessages.WM_COMPAREITEM
    WM_CONTEXTMENU = CSWindowsMessages.WM_CONTEXTMENU
    WM_COPY = CSWindowsMessages.WM_COPY
    WM_COPYDATA = CSWindowsMessages.WM_COPYDATA
    WM_CREATE = CSWindowsMessages.WM_CREATE
    WM_CTLCOLORBTN = CSWindowsMessages.WM_CTLCOLORBTN
    WM_CTLCOLORDLG = CSWindowsMessages.WM_CTLCOLORDLG
    WM_CTLCOLOREDIT = CSWindowsMessages.WM_CTLCOLOREDIT
    WM_CTLCOLORLISTBOX = CSWindowsMessages.WM_CTLCOLORLISTBOX
    WM_CTLCOLORMSGBOX = CSWindowsMessages.WM_CTLCOLORMSGBOX
    WM_CTLCOLORSCROLLBAR = CSWindowsMessages.WM_CTLCOLORSCROLLBAR
    WM_CTLCOLORSTATIC = CSWindowsMessages.WM_CTLCOLORSTATIC
    WM_CUT = CSWindowsMessages.WM_CUT
    WM_DEADCHAR = CSWindowsMessages.WM_DEADCHAR
    WM_DELETEITEM = CSWindowsMessages.WM_DELETEITEM
    WM_DESTROY = CSWindowsMessages.WM_DESTROY
    WM_DESTROYCLIPBOARD = CSWindowsMessages.WM_DESTROYCLIPBOARD
    WM_DEVICECHANGE = CSWindowsMessages.WM_DEVICECHANGE
    WM_DEVMODECHANGE = CSWindowsMessages.WM_DEVMODECHANGE
    WM_DISPLAYCHANGE = CSWindowsMessages.WM_DISPLAYCHANGE
    WM_DRAWCLIPBOARD = CSWindowsMessages.WM_DRAWCLIPBOARD
    WM_DRAWITEM = CSWindowsMessages.WM_DRAWITEM
    WM_DROPFILES = CSWindowsMessages.WM_DROPFILES
    WM_ENABLE = CSWindowsMessages.WM_ENABLE
    WM_ENDSESSION = CSWindowsMessages.WM_ENDSESSION
    WM_ENTERIDLE = CSWindowsMessages.WM_ENTERIDLE
    WM_ENTERMENULOOP = CSWindowsMessages.WM_ENTERMENULOOP
    WM_ENTERSIZEMOVE = CSWindowsMessages.WM_ENTERSIZEMOVE
    WM_ERASEBKGND = CSWindowsMessages.WM_ERASEBKGND
    WM_EXITMENULOOP = CSWindowsMessages.WM_EXITMENULOOP
    WM_EXITSIZEMOVE = CSWindowsMessages.WM_EXITSIZEMOVE
    WM_FONTCHANGE = CSWindowsMessages.WM_FONTCHANGE
    WM_GETDLGCODE = CSWindowsMessages.WM_GETDLGCODE
    WM_GETFONT = CSWindowsMessages.WM_GETFONT
    WM_GETHOTKEY = CSWindowsMessages.WM_GETHOTKEY
    WM_GETICON = CSWindowsMessages.WM_GETICON
    WM_GETMINMAXINFO = CSWindowsMessages.WM_GETMINMAXINFO
    WM_GETOBJECT = CSWindowsMessages.WM_GETOBJECT
    WM_GETTEXT = CSWindowsMessages.WM_GETTEXT
    WM_GETTEXTLENGTH = CSWindowsMessages.WM_GETTEXTLENGTH
    WM_HANDHELDFIRST = CSWindowsMessages.WM_HANDHELDFIRST
    WM_HANDHELDLAST = CSWindowsMessages.WM_HANDHELDLAST
    WM_HELP = CSWindowsMessages.WM_HELP
    WM_HOTKEY = CSWindowsMessages.WM_HOTKEY
    WM_HSCROLL = CSWindowsMessages.WM_HSCROLL
    WM_HSCROLLCLIPBOARD = CSWindowsMessages.WM_HSCROLLCLIPBOARD
    WM_ICONERASEBKGND = CSWindowsMessages.WM_ICONERASEBKGND
    WM_IME_CHAR = CSWindowsMessages.WM_IME_CHAR
    WM_IME_COMPOSITION = CSWindowsMessages.WM_IME_COMPOSITION
    WM_IME_COMPOSITIONFULL = CSWindowsMessages.WM_IME_COMPOSITIONFULL
    WM_IME_CONTROL = CSWindowsMessages.WM_IME_CONTROL
    WM_IME_ENDCOMPOSITION = CSWindowsMessages.WM_IME_ENDCOMPOSITION
    WM_IME_KEYDOWN = CSWindowsMessages.WM_IME_KEYDOWN
    WM_IME_KEYLAST = CSWindowsMessages.WM_IME_KEYLAST
    WM_IME_KEYUP = CSWindowsMessages.WM_IME_KEYUP
    WM_IME_NOTIFY = CSWindowsMessages.WM_IME_NOTIFY
    WM_IME_REQUEST = CSWindowsMessages.WM_IME_REQUEST
    WM_IME_SELECT = CSWindowsMessages.WM_IME_SELECT
    WM_IME_SETCONTEXT = CSWindowsMessages.WM_IME_SETCONTEXT
    WM_IME_STARTCOMPOSITION = CSWindowsMessages.WM_IME_STARTCOMPOSITION
    WM_INITDIALOG = CSWindowsMessages.WM_INITDIALOG
    WM_INITMENU = CSWindowsMessages.WM_INITMENU
    WM_INITMENUPOPUP = CSWindowsMessages.WM_INITMENUPOPUP
    WM_INPUT = CSWindowsMessages.WM_INPUT
    WM_INPUTLANGCHANGE = CSWindowsMessages.WM_INPUTLANGCHANGE
    WM_INPUTLANGCHANGEREQUEST = CSWindowsMessages.WM_INPUTLANGCHANGEREQUEST
    WM_KEYDOWN = CSWindowsMessages.WM_KEYDOWN
    WM_KEYFIRST = CSWindowsMessages.WM_KEYFIRST
    WM_KEYLAST = CSWindowsMessages.WM_KEYLAST
    WM_KEYUP = CSWindowsMessages.WM_KEYUP
    WM_KILLFOCUS = CSWindowsMessages.WM_KILLFOCUS
    WM_LBUTTONDBLCLK = CSWindowsMessages.WM_LBUTTONDBLCLK
    WM_LBUTTONDOWN = CSWindowsMessages.WM_LBUTTONDOWN
    WM_LBUTTONUP = CSWindowsMessages.WM_LBUTTONUP
    WM_MBUTTONDBLCLK = CSWindowsMessages.WM_MBUTTONDBLCLK
    WM_MBUTTONDOWN = CSWindowsMessages.WM_MBUTTONDOWN
    WM_MBUTTONUP = CSWindowsMessages.WM_MBUTTONUP
    WM_MDIACTIVATE = CSWindowsMessages.WM_MDIACTIVATE
    WM_MDICASCADE = CSWindowsMessages.WM_MDICASCADE
    WM_MDICREATE = CSWindowsMessages.WM_MDICREATE
    WM_MDIDESTROY = CSWindowsMessages.WM_MDIDESTROY
    WM_MDIGETACTIVE = CSWindowsMessages.WM_MDIGETACTIVE
    WM_MDIICONARRANGE = CSWindowsMessages.WM_MDIICONARRANGE
    WM_MDIMAXIMIZE = CSWindowsMessages.WM_MDIMAXIMIZE
    WM_MDINEXT = CSWindowsMessages.WM_MDINEXT
    WM_MDIREFRESHMENU = CSWindowsMessages.WM_MDIREFRESHMENU
    WM_MDIRESTORE = CSWindowsMessages.WM_MDIRESTORE
    WM_MDISETMENU = CSWindowsMessages.WM_MDISETMENU
    WM_MDITILE = CSWindowsMessages.WM_MDITILE
    WM_MEASUREITEM = CSWindowsMessages.WM_MEASUREITEM
    WM_MENUCHAR = CSWindowsMessages.WM_MENUCHAR
    WM_MENUCOMMAND = CSWindowsMessages.WM_MENUCOMMAND
    WM_MENUDRAG = CSWindowsMessages.WM_MENUDRAG
    WM_MENUGETOBJECT = CSWindowsMessages.WM_MENUGETOBJECT
    WM_MENURBUTTONUP = CSWindowsMessages.WM_MENURBUTTONUP
    WM_MENUSELECT = CSWindowsMessages.WM_MENUSELECT
    WM_MOUSEACTIVATE = CSWindowsMessages.WM_MOUSEACTIVATE
    WM_MOUSEFIRST = CSWindowsMessages.WM_MOUSEFIRST
    WM_MOUSEHOVER = CSWindowsMessages.WM_MOUSEHOVER
    WM_MOUSELAST = CSWindowsMessages.WM_MOUSELAST
    WM_MOUSELEAVE = CSWindowsMessages.WM_MOUSELEAVE
    WM_MOUSEMOVE = CSWindowsMessages.WM_MOUSEMOVE
    WM_MOUSEWHEEL = CSWindowsMessages.WM_MOUSEWHEEL
    WM_MOVE = CSWindowsMessages.WM_MOVE
    WM_MOVING = CSWindowsMessages.WM_MOVING
    WM_NCACTIVATE = CSWindowsMessages.WM_NCACTIVATE
    WM_NCCALCSIZE = CSWindowsMessages.WM_NCCALCSIZE
    WM_NCCREATE = CSWindowsMessages.WM_NCCREATE
    WM_NCDESTROY = CSWindowsMessages.WM_NCDESTROY
    WM_NCHITTEST = CSWindowsMessages.WM_NCHITTEST
    WM_NCLBUTTONDBLCLK = CSWindowsMessages.WM_NCLBUTTONDBLCLK
    WM_NCLBUTTONDOWN = CSWindowsMessages.WM_NCLBUTTONDOWN
    WM_NCLBUTTONUP = CSWindowsMessages.WM_NCLBUTTONUP
    WM_NCMBUTTONDBLCLK = CSWindowsMessages.WM_NCMBUTTONDBLCLK
    WM_NCMBUTTONDOWN = CSWindowsMessages.WM_NCMBUTTONDOWN
    WM_NCMBUTTONUP = CSWindowsMessages.WM_NCMBUTTONUP
    WM_NCMOUSEHOVER = CSWindowsMessages.WM_NCMOUSEHOVER
    WM_NCMOUSELEAVE = CSWindowsMessages.WM_NCMOUSELEAVE
    WM_NCMOUSEMOVE = CSWindowsMessages.WM_NCMOUSEMOVE
    WM_NCPAINT = CSWindowsMessages.WM_NCPAINT
    WM_NCRBUTTONDBLCLK = CSWindowsMessages.WM_NCRBUTTONDBLCLK
    WM_NCRBUTTONDOWN = CSWindowsMessages.WM_NCRBUTTONDOWN
    WM_NCRBUTTONUP = CSWindowsMessages.WM_NCRBUTTONUP
    WM_NCXBUTTONDBLCLK = CSWindowsMessages.WM_NCXBUTTONDBLCLK
    WM_NCXBUTTONDOWN = CSWindowsMessages.WM_NCXBUTTONDOWN
    WM_NCXBUTTONUP = CSWindowsMessages.WM_NCXBUTTONUP
    WM_NEXTDLGCTL = CSWindowsMessages.WM_NEXTDLGCTL
    WM_NEXTMENU = CSWindowsMessages.WM_NEXTMENU
    WM_NOTIFY = CSWindowsMessages.WM_NOTIFY
    WM_NOTIFYFORMAT = CSWindowsMessages.WM_NOTIFYFORMAT
    WM_NULL = CSWindowsMessages.WM_NULL
    WM_PAINT = CSWindowsMessages.WM_PAINT
    WM_PAINTCLIPBOARD = CSWindowsMessages.WM_PAINTCLIPBOARD
    WM_PAINTICON = CSWindowsMessages.WM_PAINTICON
    WM_PALETTECHANGED = CSWindowsMessages.WM_PALETTECHANGED
    WM_PALETTEISCHANGING = CSWindowsMessages.WM_PALETTEISCHANGING
    WM_PARENTNOTIFY = CSWindowsMessages.WM_PARENTNOTIFY
    WM_PASTE = CSWindowsMessages.WM_PASTE
    WM_PENWINFIRST = CSWindowsMessages.WM_PENWINFIRST
    WM_PENWINLAST = CSWindowsMessages.WM_PENWINLAST
    WM_POWER = CSWindowsMessages.WM_POWER
    WM_POWERBROADCAST = CSWindowsMessages.WM_POWERBROADCAST
    WM_PRINT = CSWindowsMessages.WM_PRINT
    WM_PRINTCLIENT = CSWindowsMessages.WM_PRINTCLIENT
    WM_QUERYDRAGICON = CSWindowsMessages.WM_QUERYDRAGICON
    WM_QUERYENDSESSION = CSWindowsMessages.WM_QUERYENDSESSION
    WM_QUERYNEWPALETTE = CSWindowsMessages.WM_QUERYNEWPALETTE
    WM_QUERYOPEN = CSWindowsMessages.WM_QUERYOPEN
    WM_QUERYUISTATE = CSWindowsMessages.WM_QUERYUISTATE
    WM_QUEUESYNC = CSWindowsMessages.WM_QUEUESYNC
    WM_QUIT = CSWindowsMessages.WM_QUIT
    WM_RBUTTONDBLCLK = CSWindowsMessages.WM_RBUTTONDBLCLK
    WM_RBUTTONDOWN = CSWindowsMessages.WM_RBUTTONDOWN
    WM_RBUTTONUP = CSWindowsMessages.WM_RBUTTONUP
    WM_RENDERALLFORMATS = CSWindowsMessages.WM_RENDERALLFORMATS
    WM_RENDERFORMAT = CSWindowsMessages.WM_RENDERFORMAT
    WM_SETCURSOR = CSWindowsMessages.WM_SETCURSOR
    WM_SETFOCUS = CSWindowsMessages.WM_SETFOCUS
    WM_SETFONT = CSWindowsMessages.WM_SETFONT
    WM_SETHOTKEY = CSWindowsMessages.WM_SETHOTKEY
    WM_SETICON = CSWindowsMessages.WM_SETICON
    WM_SETREDRAW = CSWindowsMessages.WM_SETREDRAW
    WM_SETTEXT = CSWindowsMessages.WM_SETTEXT
    WM_SETTINGCHANGE = CSWindowsMessages.WM_SETTINGCHANGE
    WM_SHOWWINDOW = CSWindowsMessages.WM_SHOWWINDOW
    WM_SIZE = CSWindowsMessages.WM_SIZE
    WM_SIZECLIPBOARD = CSWindowsMessages.WM_SIZECLIPBOARD
    WM_SIZING = CSWindowsMessages.WM_SIZING
    WM_SPOOLERSTATUS = CSWindowsMessages.WM_SPOOLERSTATUS
    WM_STYLECHANGED = CSWindowsMessages.WM_STYLECHANGED
    WM_STYLECHANGING = CSWindowsMessages.WM_STYLECHANGING
    WM_SYNCPAINT = CSWindowsMessages.WM_SYNCPAINT
    WM_SYSCHAR = CSWindowsMessages.WM_SYSCHAR
    WM_SYSCOLORCHANGE = CSWindowsMessages.WM_SYSCOLORCHANGE
    WM_SYSCOMMAND = CSWindowsMessages.WM_SYSCOMMAND
    WM_SYSDEADCHAR = CSWindowsMessages.WM_SYSDEADCHAR
    WM_SYSKEYDOWN = CSWindowsMessages.WM_SYSKEYDOWN
    WM_SYSKEYUP = CSWindowsMessages.WM_SYSKEYUP
    WM_TABLET_FIRST = CSWindowsMessages.WM_TABLET_FIRST
    WM_TABLET_LAST = CSWindowsMessages.WM_TABLET_LAST
    WM_TCARD = CSWindowsMessages.WM_TCARD
    WM_THEMECHANGED = CSWindowsMessages.WM_THEMECHANGED
    WM_TIMECHANGE = CSWindowsMessages.WM_TIMECHANGE
    WM_TIMER = CSWindowsMessages.WM_TIMER
    WM_UNDO = CSWindowsMessages.WM_UNDO
    WM_UNICHAR = CSWindowsMessages.WM_UNICHAR
    WM_UNINITMENUPOPUP = CSWindowsMessages.WM_UNINITMENUPOPUP
    WM_UPDATEUISTATE = CSWindowsMessages.WM_UPDATEUISTATE
    WM_USER = CSWindowsMessages.WM_USER
    WM_USERCHANGED = CSWindowsMessages.WM_USERCHANGED
    WM_VKEYTOITEM = CSWindowsMessages.WM_VKEYTOITEM
    WM_VSCROLL = CSWindowsMessages.WM_VSCROLL
    WM_VSCROLLCLIPBOARD = CSWindowsMessages.WM_VSCROLLCLIPBOARD
    WM_WINDOWPOSCHANGED = CSWindowsMessages.WM_WINDOWPOSCHANGED
    WM_WINDOWPOSCHANGING = CSWindowsMessages.WM_WINDOWPOSCHANGING
    WM_WININICHANGE = CSWindowsMessages.WM_WININICHANGE
    WM_WTSSESSION_CHANGE = CSWindowsMessages.WM_WTSSESSION_CHANGE
    WM_XBUTTONDBLCLK = CSWindowsMessages.WM_XBUTTONDBLCLK
    WM_XBUTTONDOWN = CSWindowsMessages.WM_XBUTTONDOWN
    WM_XBUTTONUP = CSWindowsMessages.WM_XBUTTONUP


class WindowLongParam(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.WindowLongParam enum"""

    # TODO: Add inline description
    GWL_EXSTYLE = CSWindowLongParam.GWL_EXSTYLE
    GWL_HINSTANCE = CSWindowLongParam.GWL_HINSTANCE
    GWL_HWNDPARENT = CSWindowLongParam.GWL_HWNDPARENT
    GWL_ID = CSWindowLongParam.GWL_ID
    GWL_STYLE = CSWindowLongParam.GWL_STYLE
    GWL_USERDATA = CSWindowLongParam.GWL_USERDATA
    GWL_WNDPROC = CSWindowLongParam.GWL_WNDPROC


class WindowStyles(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.WindowStyles enum"""

    # TODO: Add inline description
    WS_BORDER = CSWindowStyles.WS_BORDER
    WS_CAPTION = CSWindowStyles.WS_CAPTION
    WS_CHILD = CSWindowStyles.WS_CHILD
    WS_CHILDWINDOW = CSWindowStyles.WS_CHILDWINDOW
    WS_CLIPCHILDREN = CSWindowStyles.WS_CLIPCHILDREN
    WS_CLIPSIBLINGS = CSWindowStyles.WS_CLIPSIBLINGS
    WS_DISABLED = CSWindowStyles.WS_DISABLED
    WS_DLGFRAME = CSWindowStyles.WS_DLGFRAME
    WS_EX_ACCEPTFILES = CSWindowStyles.WS_EX_ACCEPTFILES
    WS_EX_APPWINDOW = CSWindowStyles.WS_EX_APPWINDOW
    WS_EX_CLIENTEDGE = CSWindowStyles.WS_EX_CLIENTEDGE
    WS_EX_COMPOSITED = CSWindowStyles.WS_EX_COMPOSITED
    WS_EX_CONTEXTHELP = CSWindowStyles.WS_EX_CONTEXTHELP
    WS_EX_CONTROLPARENT = CSWindowStyles.WS_EX_CONTROLPARENT
    WS_EX_DLGMODALFRAME = CSWindowStyles.WS_EX_DLGMODALFRAME
    WS_EX_LAYERED = CSWindowStyles.WS_EX_LAYERED
    WS_EX_LAYOUTRTL = CSWindowStyles.WS_EX_LAYOUTRTL
    WS_EX_LEFT = CSWindowStyles.WS_EX_LEFT
    WS_EX_LEFTSCROLLBAR = CSWindowStyles.WS_EX_LEFTSCROLLBAR
    WS_EX_LTRREADING = CSWindowStyles.WS_EX_LTRREADING
    WS_EX_MDICHILD = CSWindowStyles.WS_EX_MDICHILD
    WS_EX_NOACTIVATE = CSWindowStyles.WS_EX_NOACTIVATE
    WS_EX_NOINHERITLAYOUT = CSWindowStyles.WS_EX_NOINHERITLAYOUT
    WS_EX_NOPARENTNOTIFY = CSWindowStyles.WS_EX_NOPARENTNOTIFY
    WS_EX_OVERLAPPEDWINDOW = CSWindowStyles.WS_EX_OVERLAPPEDWINDOW
    WS_EX_PALETTEWINDOW = CSWindowStyles.WS_EX_PALETTEWINDOW
    WS_EX_RIGHT = CSWindowStyles.WS_EX_RIGHT
    WS_EX_RIGHTSCROLLBAR = CSWindowStyles.WS_EX_RIGHTSCROLLBAR
    WS_EX_RTLREADING = CSWindowStyles.WS_EX_RTLREADING
    WS_EX_STATICEDGE = CSWindowStyles.WS_EX_STATICEDGE
    WS_EX_TOOLWINDOW = CSWindowStyles.WS_EX_TOOLWINDOW
    WS_EX_TOPMOST = CSWindowStyles.WS_EX_TOPMOST
    WS_EX_TRANSPARENT = CSWindowStyles.WS_EX_TRANSPARENT
    WS_EX_WINDOWEDGE = CSWindowStyles.WS_EX_WINDOWEDGE
    WS_GROUP = CSWindowStyles.WS_GROUP
    WS_HSCROLL = CSWindowStyles.WS_HSCROLL
    WS_ICONIC = CSWindowStyles.WS_ICONIC
    WS_MAXIMIZE = CSWindowStyles.WS_MAXIMIZE
    WS_MAXIMIZEBOX = CSWindowStyles.WS_MAXIMIZEBOX
    WS_MINIMIZE = CSWindowStyles.WS_MINIMIZE
    WS_MINIMIZEBOX = CSWindowStyles.WS_MINIMIZEBOX
    WS_OVERLAPPED = CSWindowStyles.WS_OVERLAPPED
    WS_OVERLAPPEDWINDOW = CSWindowStyles.WS_OVERLAPPEDWINDOW
    WS_POPUP = CSWindowStyles.WS_POPUP
    WS_POPUPWINDOW = CSWindowStyles.WS_POPUPWINDOW
    WS_SIZEBOX = CSWindowStyles.WS_SIZEBOX
    WS_SYSMENU = CSWindowStyles.WS_SYSMENU
    WS_TABSTOP = CSWindowStyles.WS_TABSTOP
    WS_THICKFRAME = CSWindowStyles.WS_THICKFRAME
    WS_TILED = CSWindowStyles.WS_TILED
    WS_TILEDWINDOW = CSWindowStyles.WS_TILEDWINDOW
    WS_VISIBLE = CSWindowStyles.WS_VISIBLE
    WS_VSCROLL = CSWindowStyles.WS_VSCROLL


class SetWindowPosFlags(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.SetWindowPosFlags enum"""

    # TODO: Add inline description
    SWP_ASYNCWINDOWPOS = CSSetWindowPosFlags.SWP_ASYNCWINDOWPOS
    SWP_DEFERERASE = CSSetWindowPosFlags.SWP_DEFERERASE
    SWP_DRAWFRAME = CSSetWindowPosFlags.SWP_DRAWFRAME
    SWP_FRAMECHANGED = CSSetWindowPosFlags.SWP_FRAMECHANGED
    SWP_HIDEWINDOW = CSSetWindowPosFlags.SWP_HIDEWINDOW
    SWP_NOACTIVATE = CSSetWindowPosFlags.SWP_NOACTIVATE
    SWP_NOCOPYBITS = CSSetWindowPosFlags.SWP_NOCOPYBITS
    SWP_NOMOVE = CSSetWindowPosFlags.SWP_NOMOVE
    SWP_NOOWNERZORDER = CSSetWindowPosFlags.SWP_NOOWNERZORDER
    SWP_NOREDRAW = CSSetWindowPosFlags.SWP_NOREDRAW
    SWP_NOREPOSITION = CSSetWindowPosFlags.SWP_NOREPOSITION
    SWP_NOSENDCHANGING = CSSetWindowPosFlags.SWP_NOSENDCHANGING
    SWP_NOSIZE = CSSetWindowPosFlags.SWP_NOSIZE
    SWP_NOZORDER = CSSetWindowPosFlags.SWP_NOZORDER
    SWP_SHOWWINDOW = CSSetWindowPosFlags.SWP_SHOWWINDOW


class ShowWindowTypes(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.ShowWindowTypes enum"""

    # TODO: Add inline description
    SW_FORCEMINIMIZE = CSShowWindowTypes.SW_FORCEMINIMIZE
    SW_HIDE = CSShowWindowTypes.SW_HIDE
    SW_MAX = CSShowWindowTypes.SW_MAX
    SW_MAXIMIZE = CSShowWindowTypes.SW_MAXIMIZE
    SW_MINIMIZE = CSShowWindowTypes.SW_MINIMIZE
    SW_NORMAL = CSShowWindowTypes.SW_NORMAL
    SW_RESTORE = CSShowWindowTypes.SW_RESTORE
    SW_SHOW = CSShowWindowTypes.SW_SHOW
    SW_SHOWDEFAULT = CSShowWindowTypes.SW_SHOWDEFAULT
    SW_SHOWMAXIMIZED = CSShowWindowTypes.SW_SHOWMAXIMIZED
    SW_SHOWMINIMIZED = CSShowWindowTypes.SW_SHOWMINIMIZED
    SW_SHOWMINNOACTIVE = CSShowWindowTypes.SW_SHOWMINNOACTIVE
    SW_SHOWNA = CSShowWindowTypes.SW_SHOWNA
    SW_SHOWNOACTIVATE = CSShowWindowTypes.SW_SHOWNOACTIVATE
    SW_SHOWNORMAL = CSShowWindowTypes.SW_SHOWNORMAL


class LayeredWindowAttributes(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.LayeredWindowAttributes enum"""

    # TODO: Add inline description
    LWA_ALPHA = CSLayeredWindowAttributes.LWA_ALPHA
    LWA_COLORKEY = CSLayeredWindowAttributes.LWA_COLORKEY


class SystemMetric(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.SystemMetric enum"""

    # TODO: Add inline description
    SM_ARRANGE = CSSystemMetric.SM_ARRANGE
    SM_CLEANBOOT = CSSystemMetric.SM_CLEANBOOT
    SM_CMONITORS = CSSystemMetric.SM_CMONITORS
    SM_CMOUSEBUTTONS = CSSystemMetric.SM_CMOUSEBUTTONS
    SM_CONVERTIBLESLATEMODE = CSSystemMetric.SM_CONVERTIBLESLATEMODE
    SM_CXBORDER = CSSystemMetric.SM_CXBORDER
    SM_CXCURSOR = CSSystemMetric.SM_CXCURSOR
    SM_CXDLGFRAME = CSSystemMetric.SM_CXDLGFRAME
    SM_CXDOUBLECLK = CSSystemMetric.SM_CXDOUBLECLK
    SM_CXDRAG = CSSystemMetric.SM_CXDRAG
    SM_CXEDGE = CSSystemMetric.SM_CXEDGE
    SM_CXFIXEDFRAME = CSSystemMetric.SM_CXFIXEDFRAME
    SM_CXFOCUSBORDER = CSSystemMetric.SM_CXFOCUSBORDER
    SM_CXFRAME = CSSystemMetric.SM_CXFRAME
    SM_CXFULLSCREEN = CSSystemMetric.SM_CXFULLSCREEN
    SM_CXHSCROLL = CSSystemMetric.SM_CXHSCROLL
    SM_CXHTHUMB = CSSystemMetric.SM_CXHTHUMB
    SM_CXICON = CSSystemMetric.SM_CXICON
    SM_CXICONSPACING = CSSystemMetric.SM_CXICONSPACING
    SM_CXMAXIMIZED = CSSystemMetric.SM_CXMAXIMIZED
    SM_CXMAXTRACK = CSSystemMetric.SM_CXMAXTRACK
    SM_CXMENUCHECK = CSSystemMetric.SM_CXMENUCHECK
    SM_CXMENUSIZE = CSSystemMetric.SM_CXMENUSIZE
    SM_CXMIN = CSSystemMetric.SM_CXMIN
    SM_CXMINIMIZED = CSSystemMetric.SM_CXMINIMIZED
    SM_CXMINSPACING = CSSystemMetric.SM_CXMINSPACING
    SM_CXMINTRACK = CSSystemMetric.SM_CXMINTRACK
    SM_CXPADDEDBORDER = CSSystemMetric.SM_CXPADDEDBORDER
    SM_CXSCREEN = CSSystemMetric.SM_CXSCREEN
    SM_CXSIZE = CSSystemMetric.SM_CXSIZE
    SM_CXSIZEFRAME = CSSystemMetric.SM_CXSIZEFRAME
    SM_CXSMICON = CSSystemMetric.SM_CXSMICON
    SM_CXSMSIZE = CSSystemMetric.SM_CXSMSIZE
    SM_CXVIRTUALSCREEN = CSSystemMetric.SM_CXVIRTUALSCREEN
    SM_CXVSCROLL = CSSystemMetric.SM_CXVSCROLL
    SM_CYBORDER = CSSystemMetric.SM_CYBORDER
    SM_CYCAPTION = CSSystemMetric.SM_CYCAPTION
    SM_CYCURSOR = CSSystemMetric.SM_CYCURSOR
    SM_CYDLGFRAME = CSSystemMetric.SM_CYDLGFRAME
    SM_CYDOUBLECLK = CSSystemMetric.SM_CYDOUBLECLK
    SM_CYDRAG = CSSystemMetric.SM_CYDRAG
    SM_CYEDGE = CSSystemMetric.SM_CYEDGE
    SM_CYFIXEDFRAME = CSSystemMetric.SM_CYFIXEDFRAME
    SM_CYFOCUSBORDER = CSSystemMetric.SM_CYFOCUSBORDER
    SM_CYFRAME = CSSystemMetric.SM_CYFRAME
    SM_CYFULLSCREEN = CSSystemMetric.SM_CYFULLSCREEN
    SM_CYHSCROLL = CSSystemMetric.SM_CYHSCROLL
    SM_CYICON = CSSystemMetric.SM_CYICON
    SM_CYICONSPACING = CSSystemMetric.SM_CYICONSPACING
    SM_CYKANJIWINDOW = CSSystemMetric.SM_CYKANJIWINDOW
    SM_CYMAXIMIZED = CSSystemMetric.SM_CYMAXIMIZED
    SM_CYMAXTRACK = CSSystemMetric.SM_CYMAXTRACK
    SM_CYMENU = CSSystemMetric.SM_CYMENU
    SM_CYMENUCHECK = CSSystemMetric.SM_CYMENUCHECK
    SM_CYMENUSIZE = CSSystemMetric.SM_CYMENUSIZE
    SM_CYMIN = CSSystemMetric.SM_CYMIN
    SM_CYMINIMIZED = CSSystemMetric.SM_CYMINIMIZED
    SM_CYMINSPACING = CSSystemMetric.SM_CYMINSPACING
    SM_CYMINTRACK = CSSystemMetric.SM_CYMINTRACK
    SM_CYSCREEN = CSSystemMetric.SM_CYSCREEN
    SM_CYSIZE = CSSystemMetric.SM_CYSIZE
    SM_CYSIZEFRAME = CSSystemMetric.SM_CYSIZEFRAME
    SM_CYSMCAPTION = CSSystemMetric.SM_CYSMCAPTION
    SM_CYSMICON = CSSystemMetric.SM_CYSMICON
    SM_CYSMSIZE = CSSystemMetric.SM_CYSMSIZE
    SM_CYVIRTUALSCREEN = CSSystemMetric.SM_CYVIRTUALSCREEN
    SM_CYVSCROLL = CSSystemMetric.SM_CYVSCROLL
    SM_CYVTHUMB = CSSystemMetric.SM_CYVTHUMB
    SM_DBCSENABLED = CSSystemMetric.SM_DBCSENABLED
    SM_DEBUG = CSSystemMetric.SM_DEBUG
    SM_DIGITIZER = CSSystemMetric.SM_DIGITIZER
    SM_IMMENABLED = CSSystemMetric.SM_IMMENABLED
    SM_MAXIMUMTOUCHES = CSSystemMetric.SM_MAXIMUMTOUCHES
    SM_MEDIACENTER = CSSystemMetric.SM_MEDIACENTER
    SM_MENUDROPALIGNMENT = CSSystemMetric.SM_MENUDROPALIGNMENT
    SM_MIDEASTENABLED = CSSystemMetric.SM_MIDEASTENABLED
    SM_MOUSEHORIZONTALWHEELPRESENT = CSSystemMetric.SM_MOUSEHORIZONTALWHEELPRESENT
    SM_MOUSEPRESENT = CSSystemMetric.SM_MOUSEPRESENT
    SM_MOUSEWHEELPRESENT = CSSystemMetric.SM_MOUSEWHEELPRESENT
    SM_NETWORK = CSSystemMetric.SM_NETWORK
    SM_PENWINDOWS = CSSystemMetric.SM_PENWINDOWS
    SM_REMOTECONTROL = CSSystemMetric.SM_REMOTECONTROL
    SM_REMOTESESSION = CSSystemMetric.SM_REMOTESESSION
    SM_SAMEDISPLAYFORMAT = CSSystemMetric.SM_SAMEDISPLAYFORMAT
    SM_SECURE = CSSystemMetric.SM_SECURE
    SM_SERVERR2 = CSSystemMetric.SM_SERVERR2
    SM_SHOWSOUNDS = CSSystemMetric.SM_SHOWSOUNDS
    SM_SHUTTINGDOWN = CSSystemMetric.SM_SHUTTINGDOWN
    SM_SLOWMACHINE = CSSystemMetric.SM_SLOWMACHINE
    SM_STARTER = CSSystemMetric.SM_STARTER
    SM_SWAPBUTTON = CSSystemMetric.SM_SWAPBUTTON
    SM_SYSTEMDOCKED = CSSystemMetric.SM_SYSTEMDOCKED
    SM_TABLETPC = CSSystemMetric.SM_TABLETPC
    SM_XVIRTUALSCREEN = CSSystemMetric.SM_XVIRTUALSCREEN
    SM_YVIRTUALSCREEN = CSSystemMetric.SM_YVIRTUALSCREEN


class InputType(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.InputType enum"""

    # TODO: Add inline description
    INPUT_HARDWARE = CSInputType.INPUT_HARDWARE
    INPUT_KEYBOARD = CSInputType.INPUT_KEYBOARD
    INPUT_MOUSE = CSInputType.INPUT_MOUSE


class MouseEventFlags(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.MouseEventFlags enum"""

    # TODO: Add inline description
    MOUSEEVENTF_ABSOLUTE = CSMouseEventFlags.MOUSEEVENTF_ABSOLUTE
    MOUSEEVENTF_HWHEEL = CSMouseEventFlags.MOUSEEVENTF_HWHEEL
    MOUSEEVENTF_LEFTDOWN = CSMouseEventFlags.MOUSEEVENTF_LEFTDOWN
    MOUSEEVENTF_LEFTUP = CSMouseEventFlags.MOUSEEVENTF_LEFTUP
    MOUSEEVENTF_MIDDLEDOWN = CSMouseEventFlags.MOUSEEVENTF_MIDDLEDOWN
    MOUSEEVENTF_MIDDLEUP = CSMouseEventFlags.MOUSEEVENTF_MIDDLEUP
    MOUSEEVENTF_MOVE = CSMouseEventFlags.MOUSEEVENTF_MOVE
    MOUSEEVENTF_MOVE_NOCOALESCE = CSMouseEventFlags.MOUSEEVENTF_MOVE_NOCOALESCE
    MOUSEEVENTF_RIGHTDOWN = CSMouseEventFlags.MOUSEEVENTF_RIGHTDOWN
    MOUSEEVENTF_RIGHTUP = CSMouseEventFlags.MOUSEEVENTF_RIGHTUP
    MOUSEEVENTF_VIRTUALDESK = CSMouseEventFlags.MOUSEEVENTF_VIRTUALDESK
    MOUSEEVENTF_WHEEL = CSMouseEventFlags.MOUSEEVENTF_WHEEL
    MOUSEEVENTF_XDOWN = CSMouseEventFlags.MOUSEEVENTF_XDOWN
    MOUSEEVENTF_XUP = CSMouseEventFlags.MOUSEEVENTF_XUP


class MouseEventDataXButtons(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.MouseEventDataXButtons enum"""

    # TODO: Add inline description
    NOTHING = CSMouseEventDataXButtons.NOTHING

    XBUTTON1 = CSMouseEventDataXButtons.XBUTTON1
    XBUTTON2 = CSMouseEventDataXButtons.XBUTTON2


class VkKeyScanModifiers(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.VkKeyScanModifiers enum"""

    # TODO: Add inline description
    ALT = CSVkKeyScanModifiers.ALT
    CONTROL = CSVkKeyScanModifiers.CONTROL

    Hankaku = CSVkKeyScanModifiers.Hankaku

    NONE = CSVkKeyScanModifiers.NONE

    Reserved1 = CSVkKeyScanModifiers.Reserved1
    Reserved2 = CSVkKeyScanModifiers.Reserved2
    SHIFT = CSVkKeyScanModifiers.SHIFT


class VirtualKeyShort(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.VirtualKeyShort enum"""

    # TODO: Add inline description
    ACCEPT = CSVirtualKeyShort.ACCEPT  # IME accept
    ADD = CSVirtualKeyShort.ADD  # Add key
    ALT = CSVirtualKeyShort.ALT  # ALT key
    APPS = CSVirtualKeyShort.APPS
    ATTN = CSVirtualKeyShort.ATTN
    BACK = CSVirtualKeyShort.BACK
    BROWSER_BACK = CSVirtualKeyShort.BROWSER_BACK
    BROWSER_FAVORITES = CSVirtualKeyShort.BROWSER_FAVORITES
    BROWSER_FORWARD = CSVirtualKeyShort.BROWSER_FORWARD
    BROWSER_HOME = CSVirtualKeyShort.BROWSER_HOME
    BROWSER_REFRESH = CSVirtualKeyShort.BROWSER_REFRESH
    BROWSER_SEARCH = CSVirtualKeyShort.BROWSER_SEARCH
    BROWSER_STOP = CSVirtualKeyShort.BROWSER_STOP
    CANCEL = CSVirtualKeyShort.CANCEL
    CAPITAL = CSVirtualKeyShort.CAPITAL
    CAPSLOCK = CSVirtualKeyShort.CAPSLOCK
    CLEAR = CSVirtualKeyShort.CLEAR
    CONTROL = CSVirtualKeyShort.CONTROL
    CONVERT = CSVirtualKeyShort.CONVERT
    CRSEL = CSVirtualKeyShort.CRSEL

    DECIMAL = CSVirtualKeyShort.DECIMAL
    DELETE = CSVirtualKeyShort.DELETE
    DIVIDE = CSVirtualKeyShort.DIVIDE
    DOWN = CSVirtualKeyShort.DOWN
    END = CSVirtualKeyShort.END
    ENTER = CSVirtualKeyShort.ENTER
    EREOF = CSVirtualKeyShort.EREOF
    ESC = CSVirtualKeyShort.ESC
    ESCAPE = CSVirtualKeyShort.ESCAPE
    EXECUTE = CSVirtualKeyShort.EXECUTE
    EXSEL = CSVirtualKeyShort.EXSEL

    F1 = CSVirtualKeyShort.F1
    F10 = CSVirtualKeyShort.F10
    F11 = CSVirtualKeyShort.F11
    F12 = CSVirtualKeyShort.F12
    F13 = CSVirtualKeyShort.F13
    F14 = CSVirtualKeyShort.F14
    F15 = CSVirtualKeyShort.F15
    F16 = CSVirtualKeyShort.F16
    F17 = CSVirtualKeyShort.F17
    F18 = CSVirtualKeyShort.F18
    F19 = CSVirtualKeyShort.F19
    F2 = CSVirtualKeyShort.F2
    F20 = CSVirtualKeyShort.F20
    F21 = CSVirtualKeyShort.F21
    F22 = CSVirtualKeyShort.F22
    F23 = CSVirtualKeyShort.F23
    F24 = CSVirtualKeyShort.F24
    F3 = CSVirtualKeyShort.F3
    F4 = CSVirtualKeyShort.F4
    F5 = CSVirtualKeyShort.F5
    F6 = CSVirtualKeyShort.F6
    F7 = CSVirtualKeyShort.F7
    F8 = CSVirtualKeyShort.F8
    F9 = CSVirtualKeyShort.F9
    FINAL = CSVirtualKeyShort.FINAL

    HANGUL = CSVirtualKeyShort.HANGUL
    HANJA = CSVirtualKeyShort.HANJA
    HELP = CSVirtualKeyShort.HELP
    HOME = CSVirtualKeyShort.HOME

    INSERT = CSVirtualKeyShort.INSERT

    JUNJA = CSVirtualKeyShort.JUNJA
    KANA = CSVirtualKeyShort.KANA
    KANJI = CSVirtualKeyShort.KANJI
    KEY_0 = CSVirtualKeyShort.KEY_0
    KEY_1 = CSVirtualKeyShort.KEY_1
    KEY_2 = CSVirtualKeyShort.KEY_2
    KEY_3 = CSVirtualKeyShort.KEY_3
    KEY_4 = CSVirtualKeyShort.KEY_4
    KEY_5 = CSVirtualKeyShort.KEY_5
    KEY_6 = CSVirtualKeyShort.KEY_6
    KEY_7 = CSVirtualKeyShort.KEY_7
    KEY_8 = CSVirtualKeyShort.KEY_8
    KEY_9 = CSVirtualKeyShort.KEY_9
    KEY_A = CSVirtualKeyShort.KEY_A
    KEY_B = CSVirtualKeyShort.KEY_B
    KEY_C = CSVirtualKeyShort.KEY_C
    KEY_D = CSVirtualKeyShort.KEY_D
    KEY_E = CSVirtualKeyShort.KEY_E
    KEY_F = CSVirtualKeyShort.KEY_F
    KEY_G = CSVirtualKeyShort.KEY_G
    KEY_H = CSVirtualKeyShort.KEY_H
    KEY_I = CSVirtualKeyShort.KEY_I
    KEY_J = CSVirtualKeyShort.KEY_J
    KEY_K = CSVirtualKeyShort.KEY_K
    KEY_L = CSVirtualKeyShort.KEY_L
    KEY_M = CSVirtualKeyShort.KEY_M
    KEY_N = CSVirtualKeyShort.KEY_N
    KEY_O = CSVirtualKeyShort.KEY_O
    KEY_P = CSVirtualKeyShort.KEY_P
    KEY_Q = CSVirtualKeyShort.KEY_Q
    KEY_R = CSVirtualKeyShort.KEY_R
    KEY_S = CSVirtualKeyShort.KEY_S
    KEY_T = CSVirtualKeyShort.KEY_T
    KEY_U = CSVirtualKeyShort.KEY_U
    KEY_V = CSVirtualKeyShort.KEY_V
    KEY_W = CSVirtualKeyShort.KEY_W
    KEY_X = CSVirtualKeyShort.KEY_X
    KEY_Y = CSVirtualKeyShort.KEY_Y
    KEY_Z = CSVirtualKeyShort.KEY_Z
    LAUNCH_APP1 = CSVirtualKeyShort.LAUNCH_APP1
    LAUNCH_APP2 = CSVirtualKeyShort.LAUNCH_APP2
    LAUNCH_MAIL = CSVirtualKeyShort.LAUNCH_MAIL
    LAUNCH_MEDIA_SELECT = CSVirtualKeyShort.LAUNCH_MEDIA_SELECT
    LBUTTON = CSVirtualKeyShort.LBUTTON
    LCONTROL = CSVirtualKeyShort.LCONTROL
    LEFT = CSVirtualKeyShort.LEFT
    LMENU = CSVirtualKeyShort.LMENU
    LSHIFT = CSVirtualKeyShort.LSHIFT
    LWIN = CSVirtualKeyShort.LWIN
    MBUTTON = CSVirtualKeyShort.MBUTTON
    MEDIA_NEXT_TRACK = CSVirtualKeyShort.MEDIA_NEXT_TRACK
    MEDIA_PLAY_PAUSE = CSVirtualKeyShort.MEDIA_PLAY_PAUSE
    MEDIA_PREV_TRACK = CSVirtualKeyShort.MEDIA_PREV_TRACK
    MEDIA_STOP = CSVirtualKeyShort.MEDIA_STOP
    MODECHANGE = CSVirtualKeyShort.MODECHANGE
    MULTIPLY = CSVirtualKeyShort.MULTIPLY

    NEXT = CSVirtualKeyShort.NEXT
    NONAME = CSVirtualKeyShort.NONAME
    NONCONVERT = CSVirtualKeyShort.NONCONVERT
    NUMLOCK = CSVirtualKeyShort.NUMLOCK
    NUMPAD0 = CSVirtualKeyShort.NUMPAD0
    NUMPAD1 = CSVirtualKeyShort.NUMPAD1
    NUMPAD2 = CSVirtualKeyShort.NUMPAD2
    NUMPAD3 = CSVirtualKeyShort.NUMPAD3
    NUMPAD4 = CSVirtualKeyShort.NUMPAD4
    NUMPAD5 = CSVirtualKeyShort.NUMPAD5
    NUMPAD6 = CSVirtualKeyShort.NUMPAD6
    NUMPAD7 = CSVirtualKeyShort.NUMPAD7
    NUMPAD8 = CSVirtualKeyShort.NUMPAD8
    NUMPAD9 = CSVirtualKeyShort.NUMPAD9
    OEM_1 = CSVirtualKeyShort.OEM_1
    OEM_102 = CSVirtualKeyShort.OEM_102
    OEM_2 = CSVirtualKeyShort.OEM_2
    OEM_3 = CSVirtualKeyShort.OEM_3
    OEM_4 = CSVirtualKeyShort.OEM_4
    OEM_5 = CSVirtualKeyShort.OEM_5
    OEM_6 = CSVirtualKeyShort.OEM_6
    OEM_7 = CSVirtualKeyShort.OEM_7
    OEM_8 = CSVirtualKeyShort.OEM_8
    OEM_CLEAR = CSVirtualKeyShort.OEM_CLEAR
    OEM_COMMA = CSVirtualKeyShort.OEM_COMMA
    OEM_MINUS = CSVirtualKeyShort.OEM_MINUS
    OEM_PERIOD = CSVirtualKeyShort.OEM_PERIOD
    OEM_PLUS = CSVirtualKeyShort.OEM_PLUS

    PA1 = CSVirtualKeyShort.PA1
    PACKET = CSVirtualKeyShort.PACKET
    PAUSE = CSVirtualKeyShort.PAUSE
    PLAY = CSVirtualKeyShort.PLAY
    PRINT = CSVirtualKeyShort.PRINT
    PRIOR = CSVirtualKeyShort.PRIOR
    PROCESSKEY = CSVirtualKeyShort.PROCESSKEY

    RBUTTON = CSVirtualKeyShort.RBUTTON
    RCONTROL = CSVirtualKeyShort.RCONTROL
    RETURN = CSVirtualKeyShort.RETURN
    RIGHT = CSVirtualKeyShort.RIGHT
    RMENU = CSVirtualKeyShort.RMENU
    RSHIFT = CSVirtualKeyShort.RSHIFT
    RWIN = CSVirtualKeyShort.RWIN

    SCROLL = CSVirtualKeyShort.SCROLL
    SELECT = CSVirtualKeyShort.SELECT
    SEPARATOR = CSVirtualKeyShort.SEPARATOR
    SHIFT = CSVirtualKeyShort.SHIFT
    SLEEP = CSVirtualKeyShort.SLEEP
    SNAPSHOT = CSVirtualKeyShort.SNAPSHOT
    SPACE = CSVirtualKeyShort.SPACE
    SUBTRACT = CSVirtualKeyShort.SUBTRACT
    TAB = CSVirtualKeyShort.TAB

    UP = CSVirtualKeyShort.UP
    VOLUME_DOWN = CSVirtualKeyShort.VOLUME_DOWN
    VOLUME_MUTE = CSVirtualKeyShort.VOLUME_MUTE
    VOLUME_UP = CSVirtualKeyShort.VOLUME_UP
    XBUTTON1 = CSVirtualKeyShort.XBUTTON1
    XBUTTON2 = CSVirtualKeyShort.XBUTTON2
    ZOOM = CSVirtualKeyShort.ZOOM


class ScanCodeShort(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.ScanCodeShort enum"""

    # TODO: Add inline description
    ADD = CSScanCodeShort.ADD
    ALT = CSScanCodeShort.ALT
    BACK = CSScanCodeShort.BACK
    CAPSLOCK = CSScanCodeShort.CAPSLOCK
    CLOSEBRACKET = CSScanCodeShort.CLOSEBRACKET
    COMMA = CSScanCodeShort.COMMA
    CONTROL = CSScanCodeShort.CONTROL

    DELETE = CSScanCodeShort.DELETE
    DIVIDE = CSScanCodeShort.DIVIDE
    ENTER = CSScanCodeShort.ENTER
    ESC = CSScanCodeShort.ESC
    ESCAPE = CSScanCodeShort.ESCAPE

    F1 = CSScanCodeShort.F1
    F10 = CSScanCodeShort.F10
    F11 = CSScanCodeShort.F11
    F12 = CSScanCodeShort.F12
    F13 = CSScanCodeShort.F13
    F14 = CSScanCodeShort.F14
    F15 = CSScanCodeShort.F15
    F16 = CSScanCodeShort.F16
    F17 = CSScanCodeShort.F17
    F18 = CSScanCodeShort.F18
    F19 = CSScanCodeShort.F19
    F2 = CSScanCodeShort.F2
    F20 = CSScanCodeShort.F20
    F21 = CSScanCodeShort.F21
    F22 = CSScanCodeShort.F22
    F23 = CSScanCodeShort.F23
    F24 = CSScanCodeShort.F24
    F3 = CSScanCodeShort.F3
    F4 = CSScanCodeShort.F4
    F5 = CSScanCodeShort.F5
    F6 = CSScanCodeShort.F6
    F7 = CSScanCodeShort.F7
    F8 = CSScanCodeShort.F8
    F9 = CSScanCodeShort.F9

    HELP = CSScanCodeShort.HELP

    KEY_0 = CSScanCodeShort.KEY_0
    KEY_1 = CSScanCodeShort.KEY_1
    KEY_2 = CSScanCodeShort.KEY_2
    KEY_3 = CSScanCodeShort.KEY_3
    KEY_4 = CSScanCodeShort.KEY_4
    KEY_5 = CSScanCodeShort.KEY_5
    KEY_6 = CSScanCodeShort.KEY_6
    KEY_7 = CSScanCodeShort.KEY_7
    KEY_8 = CSScanCodeShort.KEY_8
    KEY_9 = CSScanCodeShort.KEY_9
    KEY_A = CSScanCodeShort.KEY_A
    KEY_B = CSScanCodeShort.KEY_B
    KEY_C = CSScanCodeShort.KEY_C
    KEY_D = CSScanCodeShort.KEY_D
    KEY_E = CSScanCodeShort.KEY_E
    KEY_F = CSScanCodeShort.KEY_F
    KEY_G = CSScanCodeShort.KEY_G
    KEY_H = CSScanCodeShort.KEY_H
    KEY_I = CSScanCodeShort.KEY_I
    KEY_J = CSScanCodeShort.KEY_J
    KEY_K = CSScanCodeShort.KEY_K
    KEY_L = CSScanCodeShort.KEY_L
    KEY_M = CSScanCodeShort.KEY_M
    KEY_N = CSScanCodeShort.KEY_N
    KEY_O = CSScanCodeShort.KEY_O
    KEY_P = CSScanCodeShort.KEY_P
    KEY_Q = CSScanCodeShort.KEY_Q
    KEY_R = CSScanCodeShort.KEY_R
    KEY_S = CSScanCodeShort.KEY_S
    KEY_T = CSScanCodeShort.KEY_T
    KEY_U = CSScanCodeShort.KEY_U
    KEY_V = CSScanCodeShort.KEY_V
    KEY_W = CSScanCodeShort.KEY_W
    KEY_X = CSScanCodeShort.KEY_X
    KEY_Y = CSScanCodeShort.KEY_Y
    KEY_Z = CSScanCodeShort.KEY_Z
    LWIN = CSScanCodeShort.LWIN
    MULTIPLY = CSScanCodeShort.MULTIPLY

    NUMLOCK = CSScanCodeShort.NUMLOCK
    NUMPAD0 = CSScanCodeShort.NUMPAD0
    NUMPAD1 = CSScanCodeShort.NUMPAD1
    NUMPAD2 = CSScanCodeShort.NUMPAD2
    NUMPAD3 = CSScanCodeShort.NUMPAD3
    NUMPAD4 = CSScanCodeShort.NUMPAD4
    NUMPAD5 = CSScanCodeShort.NUMPAD5
    NUMPAD6 = CSScanCodeShort.NUMPAD6
    NUMPAD7 = CSScanCodeShort.NUMPAD7
    NUMPAD8 = CSScanCodeShort.NUMPAD8
    NUMPAD9 = CSScanCodeShort.NUMPAD9
    OEM_102 = CSScanCodeShort.OEM_102
    OEM_MINUS = CSScanCodeShort.OEM_MINUS
    OEM_PLUS = CSScanCodeShort.OEM_PLUS
    OPENBRACKET = CSScanCodeShort.OPENBRACKET

    PAUSE = CSScanCodeShort.PAUSE
    PERIOD = CSScanCodeShort.PERIOD
    PIPE = CSScanCodeShort.PIPE
    POWER = CSScanCodeShort.POWER

    QUOTE = CSScanCodeShort.QUOTE
    RETURN = CSScanCodeShort.RETURN
    RSHIFT = CSScanCodeShort.RSHIFT
    RWIN = CSScanCodeShort.RWIN

    SEMICOLON = CSScanCodeShort.SEMICOLON
    SHIFT = CSScanCodeShort.SHIFT
    SLEEP = CSScanCodeShort.SLEEP
    SNAPSHOT = CSScanCodeShort.SNAPSHOT
    SPACE = CSScanCodeShort.SPACE
    SUBTRACT = CSScanCodeShort.SUBTRACT
    TAB = CSScanCodeShort.TAB
    TILDE = CSScanCodeShort.TILDE

    WINMENU = CSScanCodeShort.WINMENU
    ZOOM = CSScanCodeShort.ZOOM


class KeyEventFlags(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.KeyEventFlags enum"""

    # TODO: Add inline description
    KEYEVENTF_EXTENDEDKEY = CSKeyEventFlags.KEYEVENTF_EXTENDEDKEY
    KEYEVENTF_KEYDOWN = CSKeyEventFlags.KEYEVENTF_KEYDOWN
    KEYEVENTF_KEYUP = CSKeyEventFlags.KEYEVENTF_KEYUP
    KEYEVENTF_SCANCODE = CSKeyEventFlags.KEYEVENTF_SCANCODE
    KEYEVENTF_UNICODE = CSKeyEventFlags.KEYEVENTF_UNICODE


class SendMessageTimeoutFlags(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.SendMessageTimeoutFlags enum"""

    # TODO: Add inline description
    SMTO_ABORTIFHUNG = CSSendMessageTimeoutFlags.SMTO_ABORTIFHUNG
    SMTO_BLOCK = CSSendMessageTimeoutFlags.SMTO_BLOCK
    SMTO_ERRORONEXIT = CSSendMessageTimeoutFlags.SMTO_ERRORONEXIT
    SMTO_NORMAL = CSSendMessageTimeoutFlags.SMTO_NORMAL
    SMTO_NOTIMEOUTIFNOTHUNG = CSSendMessageTimeoutFlags.SMTO_NOTIMEOUTIFNOTHUNG


class AccessibilityState(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.AccessibilityState enum"""

    # TODO: Add inline description
    STATE_SYSTEM_ALERT_HIGH = CSAccessibilityState.STATE_SYSTEM_ALERT_HIGH
    STATE_SYSTEM_ALERT_LOW = CSAccessibilityState.STATE_SYSTEM_ALERT_LOW
    STATE_SYSTEM_ALERT_MEDIUM = CSAccessibilityState.STATE_SYSTEM_ALERT_MEDIUM
    STATE_SYSTEM_ANIMATED = CSAccessibilityState.STATE_SYSTEM_ANIMATED
    STATE_SYSTEM_BUSY = CSAccessibilityState.STATE_SYSTEM_BUSY
    STATE_SYSTEM_CHECKED = CSAccessibilityState.STATE_SYSTEM_CHECKED
    STATE_SYSTEM_COLLAPSED = CSAccessibilityState.STATE_SYSTEM_COLLAPSED
    STATE_SYSTEM_DEFAULT = CSAccessibilityState.STATE_SYSTEM_DEFAULT
    STATE_SYSTEM_EXPANDED = CSAccessibilityState.STATE_SYSTEM_EXPANDED
    STATE_SYSTEM_EXTSELECTABLE = CSAccessibilityState.STATE_SYSTEM_EXTSELECTABLE
    STATE_SYSTEM_FLOATING = CSAccessibilityState.STATE_SYSTEM_FLOATING
    STATE_SYSTEM_FOCUSABLE = CSAccessibilityState.STATE_SYSTEM_FOCUSABLE
    STATE_SYSTEM_FOCUSED = CSAccessibilityState.STATE_SYSTEM_FOCUSED
    STATE_SYSTEM_HOTTRACKED = CSAccessibilityState.STATE_SYSTEM_HOTTRACKED
    STATE_SYSTEM_INVISIBLE = CSAccessibilityState.STATE_SYSTEM_INVISIBLE
    STATE_SYSTEM_LINKED = CSAccessibilityState.STATE_SYSTEM_LINKED
    STATE_SYSTEM_MARQUEED = CSAccessibilityState.STATE_SYSTEM_MARQUEED
    STATE_SYSTEM_MIXED = CSAccessibilityState.STATE_SYSTEM_MIXED
    STATE_SYSTEM_MOVEABLE = CSAccessibilityState.STATE_SYSTEM_MOVEABLE
    STATE_SYSTEM_MULTISELECTABLE = CSAccessibilityState.STATE_SYSTEM_MULTISELECTABLE
    STATE_SYSTEM_OFFSCREEN = CSAccessibilityState.STATE_SYSTEM_OFFSCREEN
    STATE_SYSTEM_PRESSED = CSAccessibilityState.STATE_SYSTEM_PRESSED
    STATE_SYSTEM_READONLY = CSAccessibilityState.STATE_SYSTEM_READONLY
    STATE_SYSTEM_SELECTABLE = CSAccessibilityState.STATE_SYSTEM_SELECTABLE
    STATE_SYSTEM_SELECTED = CSAccessibilityState.STATE_SYSTEM_SELECTED
    STATE_SYSTEM_SELFVOICING = CSAccessibilityState.STATE_SYSTEM_SELFVOICING
    STATE_SYSTEM_SIZEABLE = CSAccessibilityState.STATE_SYSTEM_SIZEABLE
    STATE_SYSTEM_TRAVERSED = CSAccessibilityState.STATE_SYSTEM_TRAVERSED
    STATE_SYSTEM_UNAVAILABLE = CSAccessibilityState.STATE_SYSTEM_UNAVAILABLE
    STATE_SYSTEM_VALID = CSAccessibilityState.STATE_SYSTEM_VALID


class AccessibilityRole(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.AccessibilityRole enum"""

    # TODO: Add inline description
    ROLE_SYSTEM_ALERT = CSAccessibilityRole.ROLE_SYSTEM_ALERT
    ROLE_SYSTEM_ANIMATION = CSAccessibilityRole.ROLE_SYSTEM_ANIMATION
    ROLE_SYSTEM_APPLICATION = CSAccessibilityRole.ROLE_SYSTEM_APPLICATION
    ROLE_SYSTEM_BORDER = CSAccessibilityRole.ROLE_SYSTEM_BORDER
    ROLE_SYSTEM_BUTTONDROPDOWN = CSAccessibilityRole.ROLE_SYSTEM_BUTTONDROPDOWN
    ROLE_SYSTEM_BUTTONDROPDOWNGRID = CSAccessibilityRole.ROLE_SYSTEM_BUTTONDROPDOWNGRID
    ROLE_SYSTEM_BUTTONMENU = CSAccessibilityRole.ROLE_SYSTEM_BUTTONMENU
    ROLE_SYSTEM_CARET = CSAccessibilityRole.ROLE_SYSTEM_CARET
    ROLE_SYSTEM_CELL = CSAccessibilityRole.ROLE_SYSTEM_CELL
    ROLE_SYSTEM_CHARACTER = CSAccessibilityRole.ROLE_SYSTEM_CHARACTER
    ROLE_SYSTEM_CHART = CSAccessibilityRole.ROLE_SYSTEM_CHART
    ROLE_SYSTEM_CHECKBUTTON = CSAccessibilityRole.ROLE_SYSTEM_CHECKBUTTON
    ROLE_SYSTEM_CLIENT = CSAccessibilityRole.ROLE_SYSTEM_CLIENT
    ROLE_SYSTEM_CLOCK = CSAccessibilityRole.ROLE_SYSTEM_CLOCK
    ROLE_SYSTEM_COLUMN = CSAccessibilityRole.ROLE_SYSTEM_COLUMN
    ROLE_SYSTEM_COLUMNHEADER = CSAccessibilityRole.ROLE_SYSTEM_COLUMNHEADER
    ROLE_SYSTEM_COMBOBOX = CSAccessibilityRole.ROLE_SYSTEM_COMBOBOX
    ROLE_SYSTEM_CURSOR = CSAccessibilityRole.ROLE_SYSTEM_CURSOR
    ROLE_SYSTEM_DIAGRAM = CSAccessibilityRole.ROLE_SYSTEM_DIAGRAM
    ROLE_SYSTEM_DIAL = CSAccessibilityRole.ROLE_SYSTEM_DIAL
    ROLE_SYSTEM_DIALOG = CSAccessibilityRole.ROLE_SYSTEM_DIALOG
    ROLE_SYSTEM_DOCUMENT = CSAccessibilityRole.ROLE_SYSTEM_DOCUMENT
    ROLE_SYSTEM_DROPLIST = CSAccessibilityRole.ROLE_SYSTEM_DROPLIST
    ROLE_SYSTEM_EQUATION = CSAccessibilityRole.ROLE_SYSTEM_EQUATION
    ROLE_SYSTEM_GRAPHIC = CSAccessibilityRole.ROLE_SYSTEM_GRAPHIC
    ROLE_SYSTEM_GRIP = CSAccessibilityRole.ROLE_SYSTEM_GRIP
    ROLE_SYSTEM_GROUPING = CSAccessibilityRole.ROLE_SYSTEM_GROUPING
    ROLE_SYSTEM_HELPBALLOON = CSAccessibilityRole.ROLE_SYSTEM_HELPBALLOON
    ROLE_SYSTEM_HOTKEYFIELD = CSAccessibilityRole.ROLE_SYSTEM_HOTKEYFIELD
    ROLE_SYSTEM_INDICATOR = CSAccessibilityRole.ROLE_SYSTEM_INDICATOR
    ROLE_SYSTEM_LINK = CSAccessibilityRole.ROLE_SYSTEM_LINK
    ROLE_SYSTEM_LIST = CSAccessibilityRole.ROLE_SYSTEM_LIST
    ROLE_SYSTEM_LISTITEM = CSAccessibilityRole.ROLE_SYSTEM_LISTITEM
    ROLE_SYSTEM_MENUBAR = CSAccessibilityRole.ROLE_SYSTEM_MENUBAR
    ROLE_SYSTEM_MENUITEM = CSAccessibilityRole.ROLE_SYSTEM_MENUITEM
    ROLE_SYSTEM_MENUPOPUP = CSAccessibilityRole.ROLE_SYSTEM_MENUPOPUP
    ROLE_SYSTEM_OUTLINE = CSAccessibilityRole.ROLE_SYSTEM_OUTLINE
    ROLE_SYSTEM_OUTLINEITEM = CSAccessibilityRole.ROLE_SYSTEM_OUTLINEITEM
    ROLE_SYSTEM_PAGETAB = CSAccessibilityRole.ROLE_SYSTEM_PAGETAB
    ROLE_SYSTEM_PAGETABLIST = CSAccessibilityRole.ROLE_SYSTEM_PAGETABLIST
    ROLE_SYSTEM_PANE = CSAccessibilityRole.ROLE_SYSTEM_PANE
    ROLE_SYSTEM_PROGRESSBAR = CSAccessibilityRole.ROLE_SYSTEM_PROGRESSBAR
    ROLE_SYSTEM_PROPERTYPAGE = CSAccessibilityRole.ROLE_SYSTEM_PROPERTYPAGE
    ROLE_SYSTEM_PUSHBUTTON = CSAccessibilityRole.ROLE_SYSTEM_PUSHBUTTON
    ROLE_SYSTEM_RADIOBUTTON = CSAccessibilityRole.ROLE_SYSTEM_RADIOBUTTON
    ROLE_SYSTEM_ROW = CSAccessibilityRole.ROLE_SYSTEM_ROW
    ROLE_SYSTEM_ROWHEADER = CSAccessibilityRole.ROLE_SYSTEM_ROWHEADER
    ROLE_SYSTEM_SCROLLBAR = CSAccessibilityRole.ROLE_SYSTEM_SCROLLBAR
    ROLE_SYSTEM_SEPARATOR = CSAccessibilityRole.ROLE_SYSTEM_SEPARATOR
    ROLE_SYSTEM_SLIDER = CSAccessibilityRole.ROLE_SYSTEM_SLIDER
    ROLE_SYSTEM_SOUND = CSAccessibilityRole.ROLE_SYSTEM_SOUND
    ROLE_SYSTEM_SPINBUTTON = CSAccessibilityRole.ROLE_SYSTEM_SPINBUTTON
    ROLE_SYSTEM_STATICTEXT = CSAccessibilityRole.ROLE_SYSTEM_STATICTEXT
    ROLE_SYSTEM_STATUSBAR = CSAccessibilityRole.ROLE_SYSTEM_STATUSBAR
    ROLE_SYSTEM_TABLE = CSAccessibilityRole.ROLE_SYSTEM_TABLE
    ROLE_SYSTEM_TEXT = CSAccessibilityRole.ROLE_SYSTEM_TEXT
    ROLE_SYSTEM_TITLEBAR = CSAccessibilityRole.ROLE_SYSTEM_TITLEBAR
    ROLE_SYSTEM_TOOLBAR = CSAccessibilityRole.ROLE_SYSTEM_TOOLBAR
    ROLE_SYSTEM_TOOLTIP = CSAccessibilityRole.ROLE_SYSTEM_TOOLTIP
    ROLE_SYSTEM_WHITESPACE = CSAccessibilityRole.ROLE_SYSTEM_WHITESPACE
    ROLE_SYSTEM_WINDOW = CSAccessibilityRole.ROLE_SYSTEM_WINDOW


class CursorState(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.CursorState enum"""

    # TODO: Add inline description
    CURSOR_HIDING = CSCursorState.CURSOR_HIDING
    CURSOR_SHOWING = CSCursorState.CURSOR_SHOWING
    CURSOR_SUPPRESSED = CSCursorState.CURSOR_SUPPRESSED


class StretchMode(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.StretchMode enum"""

    # TODO: Add inline description
    STRETCH_ANDSCANS = CSStretchMode.STRETCH_ANDSCANS
    STRETCH_DELETESCANS = CSStretchMode.STRETCH_DELETESCANS
    STRETCH_HALFTONE = CSStretchMode.STRETCH_HALFTONE
    STRETCH_ORSCANS = CSStretchMode.STRETCH_ORSCANS


class TernaryRasterOperations(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.TernaryRasterOperations enum"""

    # TODO: Add inline description
    BLACKNESS = CSTernaryRasterOperations.BLACKNESS
    CAPTUREBLT = CSTernaryRasterOperations.CAPTUREBLT

    DSTINVERT = CSTernaryRasterOperations.DSTINVERT

    MERGECOPY = CSTernaryRasterOperations.MERGECOPY
    MERGEPAINT = CSTernaryRasterOperations.MERGEPAINT

    NOTSRCCOPY = CSTernaryRasterOperations.NOTSRCCOPY
    NOTSRCERASE = CSTernaryRasterOperations.NOTSRCERASE

    PATCOPY = CSTernaryRasterOperations.PATCOPY
    PATINVERT = CSTernaryRasterOperations.PATINVERT
    PATPAINT = CSTernaryRasterOperations.PATPAINT

    SRCAND = CSTernaryRasterOperations.SRCAND
    SRCCOPY = CSTernaryRasterOperations.SRCCOPY
    SRCERASE = CSTernaryRasterOperations.SRCERASE
    SRCINVERT = CSTernaryRasterOperations.SRCINVERT
    SRCPAINT = CSTernaryRasterOperations.SRCPAINT

    WHITENESS = CSTernaryRasterOperations.WHITENESS


class InjectedInputVisualizationMode(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.InjectedInputVisualizationMode enum"""

    # TODO: Add inline description
    DEFAULT = CSInjectedInputVisualizationMode.DEFAULT

    INDIREC = CSInjectedInputVisualizationMode.INDIREC

    NONE = CSInjectedInputVisualizationMode.NONE


class PointerInputType(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.PointerInputType enum"""

    # TODO: Add inline description
    PT_MOUSE = CSPointerInputType.PT_MOUSE
    PT_PEN = CSPointerInputType.PT_PEN
    PT_POINTER = CSPointerInputType.PT_POINTER
    PT_TOUCH = CSPointerInputType.PT_TOUCH
    PT_TOUCHPAD = CSPointerInputType.PT_TOUCHPAD


class PointerFlags(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.PointerFlags enum"""

    # TODO: Add inline description
    CANCELLED = CSPointerFlags.CANCELLED
    CAPTURECHANGED = CSPointerFlags.CAPTURECHANGED
    CONFIDENCE = CSPointerFlags.CONFIDENCE

    DOWN = CSPointerFlags.DOWN

    FIFTHBUTTON = CSPointerFlags.FIFTHBUTTON
    FIRSTBUTTON = CSPointerFlags.FIRSTBUTTON
    FOURTHBUTTON = CSPointerFlags.FOURTHBUTTON

    HASTRANSFORM = CSPointerFlags.HASTRANSFORM
    HWHEEL = CSPointerFlags.HWHEEL

    INCONTACT = CSPointerFlags.INCONTACT
    INRANGE = CSPointerFlags.INRANGE

    NEW = CSPointerFlags.NEW
    NONE = CSPointerFlags.NONE

    PRIMARY = CSPointerFlags.PRIMARY

    SECONDBUTTON = CSPointerFlags.SECONDBUTTON
    THIRDBUTTON = CSPointerFlags.THIRDBUTTON

    UP = CSPointerFlags.UP
    UPDATE = CSPointerFlags.UPDATE
    WHEEL = CSPointerFlags.WHEEL


class PointerButtonChangeType(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.PointerButtonChangeType enum"""

    # TODO: Add inline description
    FIFTHBUTTON_DOWN = CSPointerButtonChangeType.FIFTHBUTTON_DOWN
    FIFTHBUTTON_UP = CSPointerButtonChangeType.FIFTHBUTTON_UP
    FIRSTBUTTON_DOWN = CSPointerButtonChangeType.FIRSTBUTTON_DOWN
    FIRSTBUTTON_UP = CSPointerButtonChangeType.FIRSTBUTTON_UP
    FOURTHBUTTON_DOWN = CSPointerButtonChangeType.FOURTHBUTTON_DOWN
    FOURTHBUTTON_UP = CSPointerButtonChangeType.FOURTHBUTTON_UP

    NONE = CSPointerButtonChangeType.NONE

    SECONDBUTTON_DOWN = CSPointerButtonChangeType.SECONDBUTTON_DOWN
    SECONDBUTTON_UP = CSPointerButtonChangeType.SECONDBUTTON_UP
    THIRDBUTTON_DOWN = CSPointerButtonChangeType.THIRDBUTTON_DOWN
    THIRDBUTTON_UP = CSPointerButtonChangeType.THIRDBUTTON_UP


class TouchFlags(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.TouchFlags enum"""

    # TODO: Add inline description
    NONE = CSTouchFlags.NONE


class TouchMask(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.TouchMask enum"""

    # TODO: Add inline description
    CONTACTAREA = CSTouchMask.CONTACTAREA

    NONE = CSTouchMask.NONE
    ORIENTATION = CSTouchMask.ORIENTATION

    PRESSURE = CSTouchMask.PRESSURE


class ProcessAccessFlags(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.ProcessAccessFlags enum"""

    # TODO: Add inline description
    All = CSProcessAccessFlags.All

    CreateProcess = CSProcessAccessFlags.CreateProcess
    CreateThread = CSProcessAccessFlags.CreateThread
    DuplicateHandle = CSProcessAccessFlags.DuplicateHandle

    QueryInformation = CSProcessAccessFlags.QueryInformation
    QueryLimitedInformation = CSProcessAccessFlags.QueryLimitedInformation

    SetInformation = CSProcessAccessFlags.SetInformation
    SetQuota = CSProcessAccessFlags.SetQuota
    Synchronize = CSProcessAccessFlags.Synchronize
    Terminate = CSProcessAccessFlags.Terminate

    VirtualMemoryOperation = CSProcessAccessFlags.VirtualMemoryOperation
    VirtualMemoryRead = CSProcessAccessFlags.VirtualMemoryRead
    VirtualMemoryWrite = CSProcessAccessFlags.VirtualMemoryWrite


class AllocationType(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.AllocationType enum"""

    # TODO: Add inline description
    Commit = CSAllocationType.Commit

    Decommit = CSAllocationType.Decommit

    LargePages = CSAllocationType.LargePages

    Physical = CSAllocationType.Physical

    Release = CSAllocationType.Release
    Reserve = CSAllocationType.Reserve
    Reset = CSAllocationType.Reset

    TopDown = CSAllocationType.TopDown

    WriteWatch = CSAllocationType.WriteWatch


class MemoryProtection(Enum):
    """Wrapper class for FlaUI.Core.WindowsAPI.MemoryProtection enum"""

    # TODO: Add inline description
    Execute = CSMemoryProtection.Execute
    ExecuteRead = CSMemoryProtection.ExecuteRead
    ExecuteReadWrite = CSMemoryProtection.ExecuteReadWrite
    ExecuteWriteCopy = CSMemoryProtection.ExecuteWriteCopy

    GuardModifierflag = CSMemoryProtection.GuardModifierflag

    NoAccess = CSMemoryProtection.NoAccess
    NoCacheModifierflag = CSMemoryProtection.NoCacheModifierflag

    ReadOnly = CSMemoryProtection.ReadOnly
    ReadWrite = CSMemoryProtection.ReadWrite

    WriteCombineModifierflag = CSMemoryProtection.WriteCombineModifierflag
    WriteCopy = CSMemoryProtection.WriteCopy
