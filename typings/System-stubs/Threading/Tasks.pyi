from __future__ import annotations

# stdlib
from enum import Enum
from typing import Any, List, Type

# 3rd party
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
import System.Xml
import System.Xml.Schema
import System.Xml.Serialization
from System.ComponentModel import MarshalByValueComponent

class Task:
	def __init__(self, *args, **kwargs) -> Any: ...

	@property
	def AsyncState(self): ...

	@AsyncState.setter
	def AsyncState(self, value): ...

	def CompletedTask(self, *args, **kwargs) -> Any: ...

	def ConfigureAwait(
			self,
			_: bool,
			) -> System.Runtime.CompilerServices.ConfiguredTaskAwaitable: ...

	def ContinueWith(
			self,
			_: System.Action[Task, object],
			__: object,
			___: System.Threading.CancellationToken,
			____: TaskContinuationOptions,
			_____: TaskScheduler,
			) -> Task: ...

	@property
	def CreationOptions(self): ...

	@CreationOptions.setter
	def CreationOptions(self, value): ...

	def CurrentId(self, *args, **kwargs) -> Any: ...

	def Delay(
			self,
			_: int,
			__: System.Threading.CancellationToken,
			) -> Task: ...

	def Dispose(self, _: bool) -> None: ...
	def Equals(self, _: object, __: object) -> bool: ...

	@property
	def Exception(self): ...

	@Exception.setter
	def Exception(self, value): ...

	def Factory(self, *args, **kwargs) -> Any: ...
	def Finalize(self) -> None: ...

	def FromCanceled(
			self,
			_: System.Threading.CancellationToken,
			) -> Task: ...

	def FromException(self, _: Exception) -> Task: ...
	def FromResult(self, *args, **kwargs) -> Any: ...
	def GetAwaiter(self) -> System.Runtime.CompilerServices.TaskAwaiter: ...
	def GetHashCode(self) -> int: ...
	def GetType(self) -> Type: ...

	@property
	def Id(self): ...

	@Id.setter
	def Id(self, value): ...

	@property
	def IsCanceled(self): ...

	@IsCanceled.setter
	def IsCanceled(self, value): ...

	@property
	def IsCompleted(self): ...

	@IsCompleted.setter
	def IsCompleted(self, value): ...

	@property
	def IsFaulted(self): ...

	@IsFaulted.setter
	def IsFaulted(self, value): ...

	def MemberwiseClone(self) -> object: ...
	def Overloads(self, *args, **kwargs) -> Any: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...

	def Run(
			self,
			_: System.Func[Task],
			__: System.Threading.CancellationToken,
			) -> Task: ...

	def RunSynchronously(self, _: TaskScheduler) -> None: ...
	def Start(self, _: TaskScheduler) -> None: ...

	@property
	def Status(self): ...

	@Status.setter
	def Status(self, value): ...

	def ToString(self) -> str: ...
	def Wait(self, _: int, __: System.Threading.CancellationToken) -> bool: ...

	def WaitAll(
			self,
			_: List[Task],
			__: int,
			___: System.Threading.CancellationToken,
			) -> bool: ...

	def WaitAny(
			self,
			_: List[Task],
			__: int,
			___: System.Threading.CancellationToken,
			) -> int: ...

	def WhenAll(
			self,
			_: List[Task],
			) -> Task: ...

	def WhenAny(
			self,
			_: List[Task],
			) -> Task[Task]: ...

	def Yield(self) -> System.Runtime.CompilerServices.YieldAwaitable: ...
	def get_AsyncState(self) -> object: ...
	def get_CompletedTask(self) -> Task: ...
	def get_CreationOptions(self) -> TaskCreationOptions: ...
	def get_CurrentId(self) -> Any: ...
	def get_Exception(self) -> Exception: ...
	def get_Factory(self) -> TaskFactory: ...
	def get_Id(self) -> int: ...
	def get_IsCanceled(self) -> bool: ...
	def get_IsCompleted(self) -> bool: ...
	def get_IsFaulted(self) -> bool: ...
	def get_Status(self) -> TaskStatus: ...

class TaskScheduler:
	def __init__(self, *args, **kwargs) -> Any: ...
	def Current(self, *args, **kwargs) -> Any: ...
	def Default(self, *args, **kwargs) -> Any: ...
	def Equals(self, _: object, __: object) -> bool: ...
	def Finalize(self) -> None: ...
	def FromCurrentSynchronizationContext(self) -> TaskScheduler: ...
	def GetHashCode(self) -> int: ...
	def GetScheduledTasks(self) -> List[Task]: ...
	def GetType(self) -> Type: ...

	@property
	def Id(self): ...

	@Id.setter
	def Id(self, value): ...

	@property
	def MaximumConcurrencyLevel(self): ...

	@MaximumConcurrencyLevel.setter
	def MaximumConcurrencyLevel(self, value): ...

	def MemberwiseClone(self) -> object: ...
	def Overloads(self, *args, **kwargs) -> Any: ...
	def QueueTask(self, _: Task) -> None: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def ToString(self) -> str: ...
	def TryDequeue(self, _: Task) -> bool: ...
	def TryExecuteTask(self, _: Task) -> bool: ...
	def TryExecuteTaskInline(self, _: Task, __: bool) -> bool: ...
	def UnobservedTaskException(self, *args, **kwargs) -> Any: ...
	def add_UnobservedTaskException(self, _: Any) -> None: ...
	def get_Current(self) -> TaskScheduler: ...
	def get_Default(self) -> TaskScheduler: ...
	def get_Id(self) -> int: ...
	def get_MaximumConcurrencyLevel(self) -> int: ...
	def remove_UnobservedTaskException(self, _: Any) -> None: ...

class TaskFactory:
	def __init__(self, *args, **kwargs) -> Any: ...

	@property
	def CancellationToken(self): ...

	@CancellationToken.setter
	def CancellationToken(self, value): ...

	@property
	def ContinuationOptions(self): ...

	@ContinuationOptions.setter
	def ContinuationOptions(self, value): ...

	def ContinueWhenAll(
			self,
			_: List[Task],
			__: Any,
			___: System.Threading.CancellationToken,
			____: TaskContinuationOptions,
			_____: TaskScheduler,
			) -> Task: ...

	def ContinueWhenAny(
			self,
			_: List[Task],
			__: System.Action[Task],
			___: System.Threading.CancellationToken,
			____: TaskContinuationOptions,
			_____: TaskScheduler,
			) -> Task: ...

	@property
	def CreationOptions(self): ...

	@CreationOptions.setter
	def CreationOptions(self, value): ...

	def Equals(self, _: object, __: object) -> bool: ...
	def Finalize(self) -> None: ...

	def FromAsync(
			self,
			_: System.Func[Any, object, Any],
			__: System.Action[Any],
			___: object,
			____: TaskCreationOptions,
			) -> Task: ...

	def GetHashCode(self) -> int: ...
	def GetType(self) -> Type: ...
	def MemberwiseClone(self) -> object: ...
	def Overloads(self, *args, **kwargs) -> Any: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...

	@property
	def Scheduler(self): ...

	@Scheduler.setter
	def Scheduler(self, value): ...

	def StartNew(
			self,
			_: System.Action[object],
			__: object,
			___: System.Threading.CancellationToken,
			____: TaskCreationOptions,
			_____: TaskScheduler,
			) -> Task: ...

	def ToString(self) -> str: ...
	def get_CancellationToken(self) -> System.Threading.CancellationToken: ...
	def get_ContinuationOptions(self) -> TaskContinuationOptions: ...
	def get_CreationOptions(self) -> TaskCreationOptions: ...
	def get_Scheduler(self) -> TaskScheduler: ...

class TaskCreationOptions:
	def __init__(self, *args, **kwargs) -> Any: ...
	def AttachedToParent(self, *args, **kwargs) -> Any: ...
	def CompareTo(self, _: object) -> int: ...
	def DenyChildAttach(self, *args, **kwargs) -> Any: ...
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
	def HideScheduler(self, *args, **kwargs) -> Any: ...
	def IsDefined(self, _: Type, __: object) -> bool: ...
	def LongRunning(self, *args, **kwargs) -> Any: ...
	def MemberwiseClone(self) -> object: ...
	def Overloads(self, *args, **kwargs) -> Any: ...
	def Parse(self, _: Type, __: str, ___: bool) -> object: ...
	def PreferFairness(self, *args, **kwargs) -> Any: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def RunContinuationsAsynchronously(self, *args, **kwargs) -> Any: ...
	def ToObject(self, _: Type, __: object) -> object: ...
	def ToString(self, _: str, __: Any) -> str: ...
	def TryParse(self, *args, **kwargs) -> Any: ...

class TaskStatus:
	def __init__(self, *args, **kwargs) -> Any: ...
	def Canceled(self, *args, **kwargs) -> Any: ...
	def CompareTo(self, _: object) -> int: ...
	def Created(self, *args, **kwargs) -> Any: ...
	def Equals(self, _: object) -> bool: ...
	def Faulted(self, *args, **kwargs) -> Any: ...
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
	def RanToCompletion(self, *args, **kwargs) -> Any: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def Running(self, *args, **kwargs) -> Any: ...
	def ToObject(self, _: Type, __: object) -> object: ...
	def ToString(self, _: str, __: Any) -> str: ...
	def TryParse(self, *args, **kwargs) -> Any: ...
	def WaitingForActivation(self, *args, **kwargs) -> Any: ...
	def WaitingForChildrenToComplete(self, *args, **kwargs) -> Any: ...
	def WaitingToRun(self, *args, **kwargs) -> Any: ...

class UnobservedTaskExceptionEventArgs:
	def __init__(self, *args, **kwargs) -> Any: ...
	def Empty(self, *args, **kwargs) -> Any: ...
	def Equals(self, _: object, __: object) -> bool: ...

	@property
	def Exception(self): ...

	@Exception.setter
	def Exception(self, value): ...

	def Finalize(self) -> None: ...
	def GetHashCode(self) -> int: ...
	def GetType(self) -> Type: ...
	def MemberwiseClone(self) -> object: ...

	@property
	def Observed(self): ...

	@Observed.setter
	def Observed(self, value): ...

	def Overloads(self, *args, **kwargs) -> Any: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def SetObserved(self) -> None: ...
	def ToString(self) -> str: ...
	def get_Exception(self) -> Exception: ...
	def get_Observed(self) -> bool: ...

class TaskContinuationOptions:
	def __init__(self, *args, **kwargs) -> Any: ...
	def AttachedToParent(self, *args, **kwargs) -> Any: ...
	def CompareTo(self, _: object) -> int: ...
	def DenyChildAttach(self, *args, **kwargs) -> Any: ...
	def Equals(self, _: object) -> bool: ...
	def ExecuteSynchronously(self, *args, **kwargs) -> Any: ...
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
	def HideScheduler(self, *args, **kwargs) -> Any: ...
	def IsDefined(self, _: Type, __: object) -> bool: ...
	def LazyCancellation(self, *args, **kwargs) -> Any: ...
	def LongRunning(self, *args, **kwargs) -> Any: ...
	def MemberwiseClone(self) -> object: ...
	def NotOnCanceled(self, *args, **kwargs) -> Any: ...
	def NotOnFaulted(self, *args, **kwargs) -> Any: ...
	def NotOnRanToCompletion(self, *args, **kwargs) -> Any: ...
	def OnlyOnCanceled(self, *args, **kwargs) -> Any: ...
	def OnlyOnFaulted(self, *args, **kwargs) -> Any: ...
	def OnlyOnRanToCompletion(self, *args, **kwargs) -> Any: ...
	def Overloads(self, *args, **kwargs) -> Any: ...
	def Parse(self, _: Type, __: str, ___: bool) -> object: ...
	def PreferFairness(self, *args, **kwargs) -> Any: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def RunContinuationsAsynchronously(self, *args, **kwargs) -> Any: ...
	def ToObject(self, _: Type, __: object) -> object: ...
	def ToString(self, _: str, __: Any) -> str: ...
	def TryParse(self, *args, **kwargs) -> Any: ...