from __future__ import annotations

from enum import Enum
from typing import Any
from typing import List
from typing import Type

import System
import System.Collections
import System.ComponentModel
import System.Configuration
import System.Configuration.Assemblies
import System.Data
import System.Globalization
import System.IO
import System.Reflection
import System.Runtime
import System.Runtime.CompilerServices
import System.Runtime.InteropServices
import System.Runtime.Remoting
import System.Runtime.Serialization
import System.Security
import System.Security.AccessControl
import System.Security.Cryptography
import System.Security.Cryptography.X509Certificates
import System.Security.Policy
import System.Security.Principal
import System.Threading
import System.Threading.Tasks
import System.Xml
import System.Xml.Schema
import System.Xml.Serialization
from System.ComponentModel import MarshalByValueComponent


class Capture:

    def __init__(self, *args, **kwargs) -> Any: ...
    def Element(self, _: AutomationElement, __: CaptureSettings) -> CaptureImage: ...

    def ElementRectangle(
            self,
            _: AutomationElement,
            __: System.Drawing.Rectangle,
            ___: CaptureSettings,
            ) -> CaptureImage: ...

    def Equals(self, _: object, __: object) -> bool: ...
    def Finalize(self) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def MainScreen(self, _: CaptureSettings) -> CaptureImage: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...

    def Rectangle(
            self,
            _: System.Drawing.Rectangle,
            __: CaptureSettings,
            ) -> CaptureImage: ...

    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def Screen(self, _: int, __: CaptureSettings) -> CaptureImage: ...

    def ScreensWithElement(
            self,
            _: AutomationElement,
            __: CaptureSettings,
            ) -> CaptureImage: ...

    def ToString(self) -> str: ...


class CaptureImage:

    def __init__(self, *args, **kwargs) -> Any: ...

    def ApplyOverlays(
            self,
            _: List[ICaptureOverlay],
            ) -> CaptureImage: ...

    @property
    def Bitmap(self): ...

    @Bitmap.setter
    def Bitmap(self, value): ...

    @property
    def BitmapImage(self): ...

    @BitmapImage.setter
    def BitmapImage(self, value): ...

    def Dispose(self) -> None: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Finalize(self) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def MemberwiseClone(self) -> object: ...

    @property
    def OriginalBounds(self): ...

    @OriginalBounds.setter
    def OriginalBounds(self, value): ...

    def Overloads(self, *args, **kwargs) -> Any: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...

    @property
    def Settings(self): ...

    @Settings.setter
    def Settings(self, value): ...

    def ToFile(self, _: str) -> None: ...
    def ToString(self) -> str: ...
    def get_Bitmap(self) -> System.Drawing.Bitmap: ...
    def get_BitmapImage(self) -> System.Windows.Media.Imaging.BitmapImage: ...
    def get_OriginalBounds(self) -> System.Drawing.Rectangle: ...
    def get_Settings(self) -> CaptureSettings: ...


class CaptureSettings:

    def __init__(self, *args, **kwargs) -> Any: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Finalize(self) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def MemberwiseClone(self) -> object: ...

    @property
    def OutputHeight(self): ...

    @OutputHeight.setter
    def OutputHeight(self, value): ...

    @property
    def OutputScale(self): ...

    @OutputScale.setter
    def OutputScale(self, value): ...

    @property
    def OutputWidth(self): ...

    @OutputWidth.setter
    def OutputWidth(self, value): ...

    def Overloads(self, *args, **kwargs) -> Any: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def ToString(self) -> str: ...
    def get_OutputHeight(self) -> int: ...
    def get_OutputScale(self) -> float: ...
    def get_OutputWidth(self) -> int: ...
    def set_OutputHeight(self, _: int) -> None: ...
    def set_OutputScale(self, _: float) -> None: ...
    def set_OutputWidth(self, _: int) -> None: ...


class CaptureUtilities:

    def __init__(self, *args, **kwargs) -> Any: ...
    def CaptureCursor(self, _: System.Drawing.Point) -> System.Drawing.Bitmap: ...
    def DeleteObject(self, _: Any) -> bool: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Finalize(self) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetScale(self, _: System.Drawing.Rectangle, __: CaptureSettings) -> float: ...
    def GetType(self) -> Type: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...

    def ScaleAccordingToSettings(
            self,
            _: int,
            __: int,
            ___: System.Drawing.Rectangle,
            ____: CaptureSettings,
            ) -> System.Drawing.Point: ...

    def ToString(self) -> str: ...


class ICaptureOverlay:

    def __init__(self, *args, **kwargs) -> Any: ...
    def Draw(self, _: System.Drawing.Graphics) -> None: ...


class InfoOverlay:

    def __init__(self, *args, **kwargs) -> Any: ...

    @property
    def CaptureImage(self): ...

    @CaptureImage.setter
    def CaptureImage(self, value): ...

    def Draw(self, _: System.Drawing.Graphics) -> None: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Finalize(self) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def MemberwiseClone(self) -> object: ...

    @property
    def OverlayBackgroundColor(self): ...

    @OverlayBackgroundColor.setter
    def OverlayBackgroundColor(self, value): ...

    @property
    def OverlayPosition(self): ...

    @OverlayPosition.setter
    def OverlayPosition(self, value): ...

    @property
    def OverlayStringFormat(self): ...

    @OverlayStringFormat.setter
    def OverlayStringFormat(self, value): ...

    @property
    def OverlayTextColor(self): ...

    @OverlayTextColor.setter
    def OverlayTextColor(self, value): ...

    @property
    def OverlayTextFont(self): ...

    @OverlayTextFont.setter
    def OverlayTextFont(self, value): ...

    def Overloads(self, *args, **kwargs) -> Any: ...

    @property
    def RecordTimeSpan(self): ...

    @RecordTimeSpan.setter
    def RecordTimeSpan(self, value): ...

    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def ToString(self) -> str: ...
    def get_CaptureImage(self) -> CaptureImage: ...
    def get_OverlayBackgroundColor(self) -> System.Drawing.Color: ...
    def get_OverlayPosition(self) -> InfoOverlayPosition: ...
    def get_OverlayStringFormat(self) -> str: ...
    def get_OverlayTextColor(self) -> System.Drawing.Color: ...
    def get_OverlayTextFont(self) -> System.Drawing.Font: ...
    def get_RecordTimeSpan(self) -> System.TimeSpan: ...
    def set_OverlayBackgroundColor(self, _: System.Drawing.Color) -> None: ...
    def set_OverlayPosition(self, _: InfoOverlayPosition) -> None: ...
    def set_OverlayStringFormat(self, _: str) -> None: ...
    def set_OverlayTextColor(self, _: System.Drawing.Color) -> None: ...
    def set_OverlayTextFont(self, _: System.Drawing.Font) -> None: ...
    def set_RecordTimeSpan(self, _: System.TimeSpan) -> None: ...


class InfoOverlayPosition:

    def __init__(self, *args, **kwargs) -> Any: ...
    def BottomCenter(self, *args, **kwargs) -> Any: ...
    def BottomLeft(self, *args, **kwargs) -> Any: ...
    def BottomRight(self, *args, **kwargs) -> Any: ...
    def CompareTo(self, _: object) -> int: ...
    def Equals(self, _: object) -> bool: ...
    def Finalize(self) -> None: ...
    def Format(self, _: Type, __: object, ___: str) -> str: ...
    def GetHashCode(self) -> int: ...
    def GetName(self, _: Type, __: object) -> str: ...
    def GetNames(self, _: Type) -> List[str]: ...
    def GetType(self) -> Type: ...
    def GetTypeCode(self) -> Any: ...
    def GetUnderlyingType(self, _: Type) -> Type: ...
    def GetValues(self, _: Type) -> List: ...
    def HasFlag(self, _: Enum) -> bool: ...
    def IsDefined(self, _: Type, __: object) -> bool: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def Parse(self, _: Type, __: str, ___: bool) -> object: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def ToObject(self, _: Type, __: object) -> object: ...
    def ToString(self, _: str, __: Any) -> str: ...
    def TopCenter(self, *args, **kwargs) -> Any: ...
    def TopLeft(self, *args, **kwargs) -> Any: ...
    def TopRight(self, *args, **kwargs) -> Any: ...
    def TryParse(self, *args, **kwargs) -> Any: ...


class MouseOverlay:

    def __init__(self, *args, **kwargs) -> Any: ...

    @property
    def CaptureImage(self): ...

    @CaptureImage.setter
    def CaptureImage(self, value): ...

    def Draw(self, _: System.Drawing.Graphics) -> None: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Finalize(self) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def ToString(self) -> str: ...
    def get_CaptureImage(self) -> CaptureImage: ...


class OverlayBase:

    def __init__(self, *args, **kwargs) -> Any: ...

    @property
    def CaptureImage(self): ...

    @CaptureImage.setter
    def CaptureImage(self, value): ...

    def Draw(self, _: System.Drawing.Graphics) -> None: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Finalize(self) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def ToString(self) -> str: ...
    def get_CaptureImage(self) -> CaptureImage: ...


class VideoFormat:

    def __init__(self, *args, **kwargs) -> Any: ...
    def CompareTo(self, _: object) -> int: ...
    def Equals(self, _: object) -> bool: ...
    def Finalize(self) -> None: ...
    def Format(self, _: Type, __: object, ___: str) -> str: ...
    def GetHashCode(self) -> int: ...
    def GetName(self, _: Type, __: object) -> str: ...
    def GetNames(self, _: Type) -> List[str]: ...
    def GetType(self) -> Type: ...
    def GetTypeCode(self) -> Any: ...
    def GetUnderlyingType(self, _: Type) -> Type: ...
    def GetValues(self, _: Type) -> List: ...
    def HasFlag(self, _: Enum) -> bool: ...
    def IsDefined(self, _: Type, __: object) -> bool: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def Parse(self, _: Type, __: str, ___: bool) -> object: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def ToObject(self, _: Type, __: object) -> object: ...
    def ToString(self, _: str, __: Any) -> str: ...
    def TryParse(self, *args, **kwargs) -> Any: ...
    def xvid(self, *args, **kwargs) -> Any: ...
    def x264(self, *args, **kwargs) -> Any: ...


class VideoRecorder:

    def __init__(self, *args, **kwargs) -> Any: ...
    def Dispose(self) -> None: ...
    def DownloadFFMpeg(self, _: str) -> System.Threading.Tasks.Task[str]: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Finalize(self) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...

    @property
    def RecordTimeSpan(self): ...

    @RecordTimeSpan.setter
    def RecordTimeSpan(self, value): ...

    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def Stop(self) -> None: ...

    @property
    def TargetVideoPath(self): ...

    @TargetVideoPath.setter
    def TargetVideoPath(self, value): ...

    def ToString(self) -> str: ...
    def get_RecordTimeSpan(self) -> System.TimeSpan: ...
    def get_TargetVideoPath(self) -> str: ...


class VideoRecorderSettings:

    def __init__(self, *args, **kwargs) -> Any: ...

    @property
    def EncodeWithLowPriority(self): ...

    @EncodeWithLowPriority.setter
    def EncodeWithLowPriority(self, value): ...

    def Equals(self, _: object, __: object) -> bool: ...
    def Finalize(self) -> None: ...

    @property
    def FrameRate(self): ...

    @FrameRate.setter
    def FrameRate(self, value): ...

    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...

    @property
    def TargetVideoPath(self): ...

    @TargetVideoPath.setter
    def TargetVideoPath(self, value): ...

    def ToString(self) -> str: ...

    @property
    def UseCompressedImages(self): ...

    @UseCompressedImages.setter
    def UseCompressedImages(self, value): ...

    @property
    def VideoFormat(self): ...

    @VideoFormat.setter
    def VideoFormat(self, value): ...

    @property
    def VideoQuality(self): ...

    @VideoQuality.setter
    def VideoQuality(self, value): ...

    @property
    def ffmpegPath(self): ...

    @ffmpegPath.setter
    def ffmpegPath(self, value): ...

    def get_EncodeWithLowPriority(self) -> bool: ...
    def get_FrameRate(self) -> int: ...
    def get_TargetVideoPath(self) -> str: ...
    def get_UseCompressedImages(self) -> bool: ...
    def get_VideoFormat(self) -> VideoFormat: ...
    def get_VideoQuality(self) -> int: ...
    def get_ffmpegPath(self) -> str: ...
    def set_EncodeWithLowPriority(self, _: bool) -> None: ...
    def set_FrameRate(self, _: int) -> None: ...
    def set_TargetVideoPath(self, _: str) -> None: ...
    def set_UseCompressedImages(self, _: bool) -> None: ...
    def set_VideoFormat(self, _: VideoFormat) -> None: ...
    def set_VideoQuality(self, _: int) -> None: ...
    def set_ffmpegPath(self, _: str) -> None: ...
