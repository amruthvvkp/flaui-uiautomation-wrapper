from __future__ import annotations

# stdlib
from typing import Any, Type

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
import System.Threading
import System.Threading.Tasks
import System.Xml
import System.Xml.Schema
import System.Xml.Serialization
from System.ComponentModel import MarshalByValueComponent

class IdentityReference:
	def __init__(self, *args, **kwargs) -> Any: ...
	def Equals(self, _: object) -> bool: ...
	def Finalize(self) -> None: ...
	def GetHashCode(self) -> int: ...
	def GetType(self) -> Type: ...
	def IsValidTargetType(self, _: Type) -> bool: ...
	def MemberwiseClone(self) -> object: ...
	def Overloads(self, *args, **kwargs) -> Any: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def ToString(self) -> str: ...
	def Translate(self, _: Type) -> IdentityReference: ...

	@property
	def Value(self): ...

	@Value.setter
	def Value(self, value): ...

	def get_Value(self) -> str: ...

	def op_Equality(
			self,
			_: IdentityReference,
			__: IdentityReference,
			) -> bool: ...

	def op_Inequality(
			self,
			_: IdentityReference,
			__: IdentityReference,
			) -> bool: ...
