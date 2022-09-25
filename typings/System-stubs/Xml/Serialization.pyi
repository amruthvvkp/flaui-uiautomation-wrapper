from __future__ import annotations

# stdlib
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
import System.Threading.Tasks
import System.Xml
import System.Xml.Schema
from System.ComponentModel import MarshalByValueComponent

class XmlSerializerNamespaces:
	def __init__(self, *args, **kwargs) -> Any: ...
	def Add(self, _: str, __: str) -> None: ...

	@property
	def Count(self): ...

	@Count.setter
	def Count(self, value): ...

	def Equals(self, _: object, __: object) -> bool: ...
	def Finalize(self) -> None: ...
	def GetHashCode(self) -> int: ...
	def GetType(self) -> Type: ...
	def MemberwiseClone(self) -> object: ...
	def Overloads(self, *args, **kwargs) -> Any: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def ToArray(self) -> List[System.Xml.XmlQualifiedName]: ...
	def ToString(self) -> str: ...
	def get_Count(self) -> int: ...
