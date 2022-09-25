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
import System.Security.Policy
import System.Security.Principal
import System.Threading
import System.Threading.Tasks
import System.Xml
import System.Xml.Schema
import System.Xml.Serialization
from System.ComponentModel import MarshalByValueComponent

class X509Certificate:
	def __init__(self, *args, **kwargs) -> Any: ...

	def CreateFromCertFile(
			self,
			_: str,
			) -> X509Certificate: ...

	def CreateFromSignedFile(
			self,
			_: str,
			) -> X509Certificate: ...

	def Dispose(self, _: bool) -> None: ...
	def Equals(self, _: object) -> bool: ...

	def Export(
			self,
			_: X509ContentType,
			__: str,
			) -> List[bytes]: ...

	def Finalize(self) -> None: ...
	def FormatDate(self, _: System.DateTime) -> str: ...

	def GetCertHash(
			self,
			_: System.Security.Cryptography.HashAlgorithmName,
			) -> List[bytes]: ...

	def GetCertHashString(
			self,
			_: System.Security.Cryptography.HashAlgorithmName,
			) -> str: ...

	def GetEffectiveDateString(self) -> str: ...
	def GetExpirationDateString(self) -> str: ...
	def GetFormat(self) -> str: ...
	def GetHashCode(self) -> int: ...
	def GetIssuerName(self) -> str: ...
	def GetKeyAlgorithm(self) -> str: ...
	def GetKeyAlgorithmParameters(self) -> List[bytes]: ...
	def GetKeyAlgorithmParametersString(self) -> str: ...
	def GetName(self) -> str: ...
	def GetPublicKey(self) -> List[bytes]: ...
	def GetPublicKeyString(self) -> str: ...
	def GetRawCertData(self) -> List[bytes]: ...
	def GetRawCertDataString(self) -> str: ...
	def GetSerialNumber(self) -> List[bytes]: ...
	def GetSerialNumberString(self) -> str: ...
	def GetType(self) -> Type: ...

	@property
	def Handle(self): ...

	@Handle.setter
	def Handle(self, value): ...

	def Import(
			self,
			_: str,
			__: str,
			___: X509KeyStorageFlags,
			) -> None: ...

	@property
	def Issuer(self): ...

	@Issuer.setter
	def Issuer(self, value): ...

	def MemberwiseClone(self) -> object: ...
	def Overloads(self, *args, **kwargs) -> Any: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def Reset(self) -> None: ...

	@property
	def Subject(self): ...

	@Subject.setter
	def Subject(self, value): ...

	def ToString(self, _: bool) -> str: ...
	def get_Handle(self) -> Any: ...
	def get_Issuer(self) -> str: ...
	def get_Subject(self) -> str: ...

class X509ContentType:
	def __init__(self, *args, **kwargs) -> Any: ...
	def Authenticode(self, *args, **kwargs) -> Any: ...
	def Cert(self, *args, **kwargs) -> Any: ...
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
	def Pfx(self, *args, **kwargs) -> Any: ...
	def Pkcs12(self, *args, **kwargs) -> Any: ...
	def Pkcs7(self, *args, **kwargs) -> Any: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def SerializedCert(self, *args, **kwargs) -> Any: ...
	def SerializedStore(self, *args, **kwargs) -> Any: ...
	def ToObject(self, _: Type, __: object) -> object: ...
	def ToString(self, _: str, __: Any) -> str: ...
	def TryParse(self, *args, **kwargs) -> Any: ...
	def Unknown(self, *args, **kwargs) -> Any: ...

class X509KeyStorageFlags:
	def __init__(self, *args, **kwargs) -> Any: ...
	def CompareTo(self, _: object) -> int: ...
	def DefaultKeySet(self, *args, **kwargs) -> Any: ...
	def EphemeralKeySet(self, *args, **kwargs) -> Any: ...
	def Equals(self, _: object) -> bool: ...
	def Exportable(self, *args, **kwargs) -> Any: ...
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
	def MachineKeySet(self, *args, **kwargs) -> Any: ...
	def MemberwiseClone(self) -> object: ...
	def Overloads(self, *args, **kwargs) -> Any: ...
	def Parse(self, _: Type, __: str, ___: bool) -> object: ...
	def PersistKeySet(self, *args, **kwargs) -> Any: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def ToObject(self, _: Type, __: object) -> object: ...
	def ToString(self, _: str, __: Any) -> str: ...
	def TryParse(self, *args, **kwargs) -> Any: ...
	def UserKeySet(self, *args, **kwargs) -> Any: ...
	def UserProtected(self, *args, **kwargs) -> Any: ...