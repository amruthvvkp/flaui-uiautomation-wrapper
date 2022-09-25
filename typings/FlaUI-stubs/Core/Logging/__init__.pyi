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


class ConsoleLogger:

    def __init__(self, *args, **kwargs) -> Any: ...
    def Debug(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Error(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Fatal(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Finalize(self) -> None: ...
    def GatedDebug(self, _: str) -> None: ...
    def GatedError(self, _: str) -> None: ...
    def GatedFatal(self, _: str) -> None: ...
    def GatedInfo(self, _: str) -> None: ...
    def GatedTrace(self, _: str) -> None: ...
    def GatedWarn(self, _: str) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def Info(self, _: str, __: Exception, ___: List[object]) -> None: ...

    @property
    def IsDebugEnabled(self): ...

    @IsDebugEnabled.setter
    def IsDebugEnabled(self, value): ...

    @property
    def IsErrorEnabled(self): ...

    @IsErrorEnabled.setter
    def IsErrorEnabled(self, value): ...

    @property
    def IsFatalEnabled(self): ...

    @IsFatalEnabled.setter
    def IsFatalEnabled(self, value): ...

    @property
    def IsInfoEnabled(self): ...

    @IsInfoEnabled.setter
    def IsInfoEnabled(self, value): ...

    @property
    def IsTraceEnabled(self): ...

    @IsTraceEnabled.setter
    def IsTraceEnabled(self, value): ...

    @property
    def IsWarnEnabled(self): ...

    @IsWarnEnabled.setter
    def IsWarnEnabled(self, value): ...

    def Log(self, _: LogLevel, __: str, ___: Exception, ____: List[object]) -> None: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def SetLevel(self, _: LogLevel) -> None: ...
    def ToString(self) -> str: ...
    def Trace(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Warn(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def get_IsDebugEnabled(self) -> bool: ...
    def get_IsErrorEnabled(self) -> bool: ...
    def get_IsFatalEnabled(self) -> bool: ...
    def get_IsInfoEnabled(self) -> bool: ...
    def get_IsTraceEnabled(self) -> bool: ...
    def get_IsWarnEnabled(self) -> bool: ...
    def set_IsDebugEnabled(self, _: bool) -> None: ...
    def set_IsErrorEnabled(self, _: bool) -> None: ...
    def set_IsFatalEnabled(self, _: bool) -> None: ...
    def set_IsInfoEnabled(self, _: bool) -> None: ...
    def set_IsTraceEnabled(self, _: bool) -> None: ...
    def set_IsWarnEnabled(self, _: bool) -> None: ...


class DebugLogger:

    def __init__(self, *args, **kwargs) -> Any: ...
    def Debug(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Error(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Fatal(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Finalize(self) -> None: ...
    def GatedDebug(self, _: str) -> None: ...
    def GatedError(self, _: str) -> None: ...
    def GatedFatal(self, _: str) -> None: ...
    def GatedInfo(self, _: str) -> None: ...
    def GatedTrace(self, _: str) -> None: ...
    def GatedWarn(self, _: str) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def Info(self, _: str, __: Exception, ___: List[object]) -> None: ...

    @property
    def IsDebugEnabled(self): ...

    @IsDebugEnabled.setter
    def IsDebugEnabled(self, value): ...

    @property
    def IsErrorEnabled(self): ...

    @IsErrorEnabled.setter
    def IsErrorEnabled(self, value): ...

    @property
    def IsFatalEnabled(self): ...

    @IsFatalEnabled.setter
    def IsFatalEnabled(self, value): ...

    @property
    def IsInfoEnabled(self): ...

    @IsInfoEnabled.setter
    def IsInfoEnabled(self, value): ...

    @property
    def IsTraceEnabled(self): ...

    @IsTraceEnabled.setter
    def IsTraceEnabled(self, value): ...

    @property
    def IsWarnEnabled(self): ...

    @IsWarnEnabled.setter
    def IsWarnEnabled(self, value): ...

    def Log(self, _: LogLevel, __: str, ___: Exception, ____: List[object]) -> None: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def SetLevel(self, _: LogLevel) -> None: ...
    def ToString(self) -> str: ...
    def Trace(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Warn(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def get_IsDebugEnabled(self) -> bool: ...
    def get_IsErrorEnabled(self) -> bool: ...
    def get_IsFatalEnabled(self) -> bool: ...
    def get_IsInfoEnabled(self) -> bool: ...
    def get_IsTraceEnabled(self) -> bool: ...
    def get_IsWarnEnabled(self) -> bool: ...
    def set_IsDebugEnabled(self, _: bool) -> None: ...
    def set_IsErrorEnabled(self, _: bool) -> None: ...
    def set_IsFatalEnabled(self, _: bool) -> None: ...
    def set_IsInfoEnabled(self, _: bool) -> None: ...
    def set_IsTraceEnabled(self, _: bool) -> None: ...
    def set_IsWarnEnabled(self, _: bool) -> None: ...


class EventLogger:

    def __init__(self, *args, **kwargs) -> Any: ...
    def Debug(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Error(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Fatal(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Finalize(self) -> None: ...
    def GatedDebug(self, _: str) -> None: ...
    def GatedError(self, _: str) -> None: ...
    def GatedFatal(self, _: str) -> None: ...
    def GatedInfo(self, _: str) -> None: ...
    def GatedTrace(self, _: str) -> None: ...
    def GatedWarn(self, _: str) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def Info(self, _: str, __: Exception, ___: List[object]) -> None: ...

    @property
    def IsDebugEnabled(self): ...

    @IsDebugEnabled.setter
    def IsDebugEnabled(self, value): ...

    @property
    def IsErrorEnabled(self): ...

    @IsErrorEnabled.setter
    def IsErrorEnabled(self, value): ...

    @property
    def IsFatalEnabled(self): ...

    @IsFatalEnabled.setter
    def IsFatalEnabled(self, value): ...

    @property
    def IsInfoEnabled(self): ...

    @IsInfoEnabled.setter
    def IsInfoEnabled(self, value): ...

    @property
    def IsTraceEnabled(self): ...

    @IsTraceEnabled.setter
    def IsTraceEnabled(self, value): ...

    @property
    def IsWarnEnabled(self): ...

    @IsWarnEnabled.setter
    def IsWarnEnabled(self, value): ...

    def Log(self, _: LogLevel, __: str, ___: Exception, ____: List[object]) -> None: ...
    def MemberwiseClone(self) -> object: ...
    def OnDebug(self, *args, **kwargs) -> Any: ...
    def OnError(self, *args, **kwargs) -> Any: ...
    def OnFatal(self, *args, **kwargs) -> Any: ...
    def OnInfo(self, *args, **kwargs) -> Any: ...
    def OnLog(self, *args, **kwargs) -> Any: ...
    def OnTrace(self, *args, **kwargs) -> Any: ...
    def OnWarn(self, *args, **kwargs) -> Any: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def SetLevel(self, _: LogLevel) -> None: ...
    def ToString(self) -> str: ...
    def Trace(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Warn(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def add_OnDebug(self, _: System.Action[str]) -> None: ...
    def add_OnError(self, _: System.Action[str]) -> None: ...
    def add_OnFatal(self, _: System.Action[str]) -> None: ...
    def add_OnInfo(self, _: System.Action[str]) -> None: ...
    def add_OnLog(self, _: System.Action[LogLevel, str]) -> None: ...
    def add_OnTrace(self, _: System.Action[str]) -> None: ...
    def add_OnWarn(self, _: System.Action[str]) -> None: ...
    def get_IsDebugEnabled(self) -> bool: ...
    def get_IsErrorEnabled(self) -> bool: ...
    def get_IsFatalEnabled(self) -> bool: ...
    def get_IsInfoEnabled(self) -> bool: ...
    def get_IsTraceEnabled(self) -> bool: ...
    def get_IsWarnEnabled(self) -> bool: ...
    def remove_OnDebug(self, _: System.Action[str]) -> None: ...
    def remove_OnError(self, _: System.Action[str]) -> None: ...
    def remove_OnFatal(self, _: System.Action[str]) -> None: ...
    def remove_OnInfo(self, _: System.Action[str]) -> None: ...
    def remove_OnLog(self, _: System.Action[LogLevel, str]) -> None: ...
    def remove_OnTrace(self, _: System.Action[str]) -> None: ...
    def remove_OnWarn(self, _: System.Action[str]) -> None: ...
    def set_IsDebugEnabled(self, _: bool) -> None: ...
    def set_IsErrorEnabled(self, _: bool) -> None: ...
    def set_IsFatalEnabled(self, _: bool) -> None: ...
    def set_IsInfoEnabled(self, _: bool) -> None: ...
    def set_IsTraceEnabled(self, _: bool) -> None: ...
    def set_IsWarnEnabled(self, _: bool) -> None: ...


class ILogger:

    def __init__(self, *args, **kwargs) -> Any: ...
    def Debug(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Error(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Fatal(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Info(self, _: str, __: Exception, ___: List[object]) -> None: ...

    @property
    def IsDebugEnabled(self): ...

    @IsDebugEnabled.setter
    def IsDebugEnabled(self, value): ...

    @property
    def IsErrorEnabled(self): ...

    @IsErrorEnabled.setter
    def IsErrorEnabled(self, value): ...

    @property
    def IsFatalEnabled(self): ...

    @IsFatalEnabled.setter
    def IsFatalEnabled(self, value): ...

    @property
    def IsInfoEnabled(self): ...

    @IsInfoEnabled.setter
    def IsInfoEnabled(self, value): ...

    @property
    def IsTraceEnabled(self): ...

    @IsTraceEnabled.setter
    def IsTraceEnabled(self, value): ...

    @property
    def IsWarnEnabled(self): ...

    @IsWarnEnabled.setter
    def IsWarnEnabled(self, value): ...

    def Log(self, _: LogLevel, __: str, ___: Exception, ____: List[object]) -> None: ...
    def SetLevel(self, _: LogLevel) -> None: ...
    def Trace(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Warn(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def get_IsDebugEnabled(self) -> bool: ...
    def get_IsErrorEnabled(self) -> bool: ...
    def get_IsFatalEnabled(self) -> bool: ...
    def get_IsInfoEnabled(self) -> bool: ...
    def get_IsTraceEnabled(self) -> bool: ...
    def get_IsWarnEnabled(self) -> bool: ...
    def set_IsDebugEnabled(self, _: bool) -> None: ...
    def set_IsErrorEnabled(self, _: bool) -> None: ...
    def set_IsFatalEnabled(self, _: bool) -> None: ...
    def set_IsInfoEnabled(self, _: bool) -> None: ...
    def set_IsTraceEnabled(self, _: bool) -> None: ...
    def set_IsWarnEnabled(self, _: bool) -> None: ...


class Logger:

    def __init__(self, *args, **kwargs) -> Any: ...
    def Default(self, *args, **kwargs) -> Any: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Finalize(self) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def ToString(self) -> str: ...
    def get_Default(self) -> ILogger: ...
    def set_Default(self, _: ILogger) -> None: ...


class LoggerBase:

    def __init__(self, *args, **kwargs) -> Any: ...
    def Debug(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Error(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Fatal(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Finalize(self) -> None: ...
    def GatedDebug(self, _: str) -> None: ...
    def GatedError(self, _: str) -> None: ...
    def GatedFatal(self, _: str) -> None: ...
    def GatedInfo(self, _: str) -> None: ...
    def GatedTrace(self, _: str) -> None: ...
    def GatedWarn(self, _: str) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def Info(self, _: str, __: Exception, ___: List[object]) -> None: ...

    @property
    def IsDebugEnabled(self): ...

    @IsDebugEnabled.setter
    def IsDebugEnabled(self, value): ...

    @property
    def IsErrorEnabled(self): ...

    @IsErrorEnabled.setter
    def IsErrorEnabled(self, value): ...

    @property
    def IsFatalEnabled(self): ...

    @IsFatalEnabled.setter
    def IsFatalEnabled(self, value): ...

    @property
    def IsInfoEnabled(self): ...

    @IsInfoEnabled.setter
    def IsInfoEnabled(self, value): ...

    @property
    def IsTraceEnabled(self): ...

    @IsTraceEnabled.setter
    def IsTraceEnabled(self, value): ...

    @property
    def IsWarnEnabled(self): ...

    @IsWarnEnabled.setter
    def IsWarnEnabled(self, value): ...

    def Log(self, _: LogLevel, __: str, ___: Exception, ____: List[object]) -> None: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def SetLevel(self, _: LogLevel) -> None: ...
    def ToString(self) -> str: ...
    def Trace(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Warn(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def get_IsDebugEnabled(self) -> bool: ...
    def get_IsErrorEnabled(self) -> bool: ...
    def get_IsFatalEnabled(self) -> bool: ...
    def get_IsInfoEnabled(self) -> bool: ...
    def get_IsTraceEnabled(self) -> bool: ...
    def get_IsWarnEnabled(self) -> bool: ...
    def set_IsDebugEnabled(self, _: bool) -> None: ...
    def set_IsErrorEnabled(self, _: bool) -> None: ...
    def set_IsFatalEnabled(self, _: bool) -> None: ...
    def set_IsInfoEnabled(self, _: bool) -> None: ...
    def set_IsTraceEnabled(self, _: bool) -> None: ...
    def set_IsWarnEnabled(self, _: bool) -> None: ...


class LogLevel:

    def __init__(self, *args, **kwargs) -> Any: ...
    def CompareTo(self, _: object) -> int: ...
    def Debug(self, *args, **kwargs) -> Any: ...
    def Equals(self, _: object) -> bool: ...
    def Error(self, *args, **kwargs) -> Any: ...
    def Fatal(self, *args, **kwargs) -> Any: ...
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
    def Info(self, *args, **kwargs) -> Any: ...
    def IsDefined(self, _: Type, __: object) -> bool: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def Parse(self, _: Type, __: str, ___: bool) -> object: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def ToObject(self, _: Type, __: object) -> object: ...
    def ToString(self, _: str, __: Any) -> str: ...
    def Trace(self, *args, **kwargs) -> Any: ...
    def TryParse(self, *args, **kwargs) -> Any: ...
    def Warn(self, *args, **kwargs) -> Any: ...


class NullLogger:

    def __init__(self, *args, **kwargs) -> Any: ...
    def Debug(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Error(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Fatal(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Finalize(self) -> None: ...
    def GatedDebug(self, _: str) -> None: ...
    def GatedError(self, _: str) -> None: ...
    def GatedFatal(self, _: str) -> None: ...
    def GatedInfo(self, _: str) -> None: ...
    def GatedTrace(self, _: str) -> None: ...
    def GatedWarn(self, _: str) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def Info(self, _: str, __: Exception, ___: List[object]) -> None: ...

    @property
    def IsDebugEnabled(self): ...

    @IsDebugEnabled.setter
    def IsDebugEnabled(self, value): ...

    @property
    def IsErrorEnabled(self): ...

    @IsErrorEnabled.setter
    def IsErrorEnabled(self, value): ...

    @property
    def IsFatalEnabled(self): ...

    @IsFatalEnabled.setter
    def IsFatalEnabled(self, value): ...

    @property
    def IsInfoEnabled(self): ...

    @IsInfoEnabled.setter
    def IsInfoEnabled(self, value): ...

    @property
    def IsTraceEnabled(self): ...

    @IsTraceEnabled.setter
    def IsTraceEnabled(self, value): ...

    @property
    def IsWarnEnabled(self): ...

    @IsWarnEnabled.setter
    def IsWarnEnabled(self, value): ...

    def Log(self, _: LogLevel, __: str, ___: Exception, ____: List[object]) -> None: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def SetLevel(self, _: LogLevel) -> None: ...
    def ToString(self) -> str: ...
    def Trace(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Warn(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def get_IsDebugEnabled(self) -> bool: ...
    def get_IsErrorEnabled(self) -> bool: ...
    def get_IsFatalEnabled(self) -> bool: ...
    def get_IsInfoEnabled(self) -> bool: ...
    def get_IsTraceEnabled(self) -> bool: ...
    def get_IsWarnEnabled(self) -> bool: ...
    def set_IsDebugEnabled(self, _: bool) -> None: ...
    def set_IsErrorEnabled(self, _: bool) -> None: ...
    def set_IsFatalEnabled(self, _: bool) -> None: ...
    def set_IsInfoEnabled(self, _: bool) -> None: ...
    def set_IsTraceEnabled(self, _: bool) -> None: ...
    def set_IsWarnEnabled(self, _: bool) -> None: ...


class TraceLogger:

    def __init__(self, *args, **kwargs) -> Any: ...
    def Debug(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Equals(self, _: object, __: object) -> bool: ...
    def Error(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Fatal(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Finalize(self) -> None: ...
    def GatedDebug(self, _: str) -> None: ...
    def GatedError(self, _: str) -> None: ...
    def GatedFatal(self, _: str) -> None: ...
    def GatedInfo(self, _: str) -> None: ...
    def GatedTrace(self, _: str) -> None: ...
    def GatedWarn(self, _: str) -> None: ...
    def GetHashCode(self) -> int: ...
    def GetType(self) -> Type: ...
    def Info(self, _: str, __: Exception, ___: List[object]) -> None: ...

    @property
    def IsDebugEnabled(self): ...

    @IsDebugEnabled.setter
    def IsDebugEnabled(self, value): ...

    @property
    def IsErrorEnabled(self): ...

    @IsErrorEnabled.setter
    def IsErrorEnabled(self, value): ...

    @property
    def IsFatalEnabled(self): ...

    @IsFatalEnabled.setter
    def IsFatalEnabled(self, value): ...

    @property
    def IsInfoEnabled(self): ...

    @IsInfoEnabled.setter
    def IsInfoEnabled(self, value): ...

    @property
    def IsTraceEnabled(self): ...

    @IsTraceEnabled.setter
    def IsTraceEnabled(self, value): ...

    @property
    def IsWarnEnabled(self): ...

    @IsWarnEnabled.setter
    def IsWarnEnabled(self, value): ...

    def Log(self, _: LogLevel, __: str, ___: Exception, ____: List[object]) -> None: ...
    def MemberwiseClone(self) -> object: ...
    def Overloads(self, *args, **kwargs) -> Any: ...
    def ReferenceEquals(self, _: object, __: object) -> bool: ...
    def SetLevel(self, _: LogLevel) -> None: ...
    def ToString(self) -> str: ...
    def Trace(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def Warn(self, _: str, __: Exception, ___: List[object]) -> None: ...
    def get_IsDebugEnabled(self) -> bool: ...
    def get_IsErrorEnabled(self) -> bool: ...
    def get_IsFatalEnabled(self) -> bool: ...
    def get_IsInfoEnabled(self) -> bool: ...
    def get_IsTraceEnabled(self) -> bool: ...
    def get_IsWarnEnabled(self) -> bool: ...
    def set_IsDebugEnabled(self, _: bool) -> None: ...
    def set_IsErrorEnabled(self, _: bool) -> None: ...
    def set_IsFatalEnabled(self, _: bool) -> None: ...
    def set_IsInfoEnabled(self, _: bool) -> None: ...
    def set_IsTraceEnabled(self, _: bool) -> None: ...
    def set_IsWarnEnabled(self, _: bool) -> None: ...
