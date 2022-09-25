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

class CultureInfo:
	def __init__(self, *args, **kwargs) -> Any: ...

	@property
	def Calendar(self): ...

	@Calendar.setter
	def Calendar(self, value): ...

	def ClearCachedData(self) -> None: ...
	def Clone(self) -> object: ...

	@property
	def CompareInfo(self): ...

	@CompareInfo.setter
	def CompareInfo(self, value): ...

	def CreateSpecificCulture(self, _: str) -> CultureInfo: ...

	@property
	def CultureTypes(self): ...

	@CultureTypes.setter
	def CultureTypes(self, value): ...

	def CurrentCulture(self, *args, **kwargs) -> Any: ...
	def CurrentUICulture(self, *args, **kwargs) -> Any: ...

	@property
	def DateTimeFormat(self): ...

	@DateTimeFormat.setter
	def DateTimeFormat(self, value): ...

	def DefaultThreadCurrentCulture(self, *args, **kwargs) -> Any: ...
	def DefaultThreadCurrentUICulture(self, *args, **kwargs) -> Any: ...

	@property
	def DisplayName(self): ...

	@DisplayName.setter
	def DisplayName(self, value): ...

	@property
	def EnglishName(self): ...

	@EnglishName.setter
	def EnglishName(self, value): ...

	def Equals(self, _: object) -> bool: ...
	def Finalize(self) -> None: ...
	def GetConsoleFallbackUICulture(self) -> CultureInfo: ...
	def GetCultureInfo(self, _: str, __: str) -> CultureInfo: ...

	def GetCultureInfoByIetfLanguageTag(
			self,
			_: str,
			) -> CultureInfo: ...

	def GetCultures(
			self,
			_: CultureTypes,
			) -> List[CultureInfo]: ...

	def GetFormat(self, _: Type) -> object: ...
	def GetHashCode(self) -> int: ...
	def GetType(self) -> Type: ...

	@property
	def IetfLanguageTag(self): ...

	@IetfLanguageTag.setter
	def IetfLanguageTag(self, value): ...

	def InstalledUICulture(self, *args, **kwargs) -> Any: ...
	def InvariantCulture(self, *args, **kwargs) -> Any: ...

	@property
	def IsNeutralCulture(self): ...

	@IsNeutralCulture.setter
	def IsNeutralCulture(self, value): ...

	@property
	def IsReadOnly(self): ...

	@IsReadOnly.setter
	def IsReadOnly(self, value): ...

	@property
	def KeyboardLayoutId(self): ...

	@KeyboardLayoutId.setter
	def KeyboardLayoutId(self, value): ...

	@property
	def LCID(self): ...

	@LCID.setter
	def LCID(self, value): ...

	def MemberwiseClone(self) -> object: ...

	@property
	def Name(self): ...

	@Name.setter
	def Name(self, value): ...

	@property
	def NativeName(self): ...

	@NativeName.setter
	def NativeName(self, value): ...

	@property
	def NumberFormat(self): ...

	@NumberFormat.setter
	def NumberFormat(self, value): ...

	@property
	def OptionalCalendars(self): ...

	@OptionalCalendars.setter
	def OptionalCalendars(self, value): ...

	def Overloads(self, *args, **kwargs) -> Any: ...

	@property
	def Parent(self): ...

	@Parent.setter
	def Parent(self, value): ...

	def ReadOnly(
			self,
			_: CultureInfo,
			) -> CultureInfo: ...

	def ReferenceEquals(self, _: object, __: object) -> bool: ...

	@property
	def TextInfo(self): ...

	@TextInfo.setter
	def TextInfo(self, value): ...

	@property
	def ThreeLetterISOLanguageName(self): ...

	@ThreeLetterISOLanguageName.setter
	def ThreeLetterISOLanguageName(self, value): ...

	@property
	def ThreeLetterWindowsLanguageName(self): ...

	@ThreeLetterWindowsLanguageName.setter
	def ThreeLetterWindowsLanguageName(self, value): ...

	def ToString(self) -> str: ...

	@property
	def TwoLetterISOLanguageName(self): ...

	@TwoLetterISOLanguageName.setter
	def TwoLetterISOLanguageName(self, value): ...

	@property
	def UseUserOverride(self): ...

	@UseUserOverride.setter
	def UseUserOverride(self, value): ...

	def get_Calendar(self) -> Calendar: ...
	def get_CompareInfo(self) -> CompareInfo: ...
	def get_CultureTypes(self) -> CultureTypes: ...
	def get_CurrentCulture(self) -> CultureInfo: ...
	def get_CurrentUICulture(self) -> CultureInfo: ...
	def get_DateTimeFormat(self) -> DateTimeFormatInfo: ...
	def get_DefaultThreadCurrentCulture(self) -> CultureInfo: ...
	def get_DefaultThreadCurrentUICulture(self) -> CultureInfo: ...
	def get_DisplayName(self) -> str: ...
	def get_EnglishName(self) -> str: ...
	def get_IetfLanguageTag(self) -> str: ...
	def get_InstalledUICulture(self) -> CultureInfo: ...
	def get_InvariantCulture(self) -> CultureInfo: ...
	def get_IsNeutralCulture(self) -> bool: ...
	def get_IsReadOnly(self) -> bool: ...
	def get_KeyboardLayoutId(self) -> int: ...
	def get_LCID(self) -> int: ...
	def get_Name(self) -> str: ...
	def get_NativeName(self) -> str: ...
	def get_NumberFormat(self) -> NumberFormatInfo: ...
	def get_OptionalCalendars(self) -> List[Calendar]: ...
	def get_Parent(self) -> CultureInfo: ...
	def get_TextInfo(self) -> TextInfo: ...
	def get_ThreeLetterISOLanguageName(self) -> str: ...
	def get_ThreeLetterWindowsLanguageName(self) -> str: ...
	def get_TwoLetterISOLanguageName(self) -> str: ...
	def get_UseUserOverride(self) -> bool: ...
	def set_CurrentCulture(self, _: CultureInfo) -> None: ...
	def set_CurrentUICulture(self, _: CultureInfo) -> None: ...
	def set_DateTimeFormat(self, _: DateTimeFormatInfo) -> None: ...

	def set_DefaultThreadCurrentCulture(
			self,
			_: CultureInfo,
			) -> None: ...

	def set_DefaultThreadCurrentUICulture(
			self,
			_: CultureInfo,
			) -> None: ...

	def set_NumberFormat(self, _: NumberFormatInfo) -> None: ...

class DateTimeFormatInfo:
	def __init__(self, *args, **kwargs) -> Any: ...

	@property
	def AMDesignator(self): ...

	@AMDesignator.setter
	def AMDesignator(self, value): ...

	@property
	def AbbreviatedDayNames(self): ...

	@AbbreviatedDayNames.setter
	def AbbreviatedDayNames(self, value): ...

	@property
	def AbbreviatedMonthGenitiveNames(self): ...

	@AbbreviatedMonthGenitiveNames.setter
	def AbbreviatedMonthGenitiveNames(self, value): ...

	@property
	def AbbreviatedMonthNames(self): ...

	@AbbreviatedMonthNames.setter
	def AbbreviatedMonthNames(self, value): ...

	@property
	def Calendar(self): ...

	@Calendar.setter
	def Calendar(self, value): ...

	@property
	def CalendarWeekRule(self): ...

	@CalendarWeekRule.setter
	def CalendarWeekRule(self, value): ...

	def Clone(self) -> object: ...
	def CurrentInfo(self, *args, **kwargs) -> Any: ...

	@property
	def DateSeparator(self): ...

	@DateSeparator.setter
	def DateSeparator(self, value): ...

	@property
	def DayNames(self): ...

	@DayNames.setter
	def DayNames(self, value): ...

	def Equals(self, _: object, __: object) -> bool: ...
	def Finalize(self) -> None: ...

	@property
	def FirstDayOfWeek(self): ...

	@FirstDayOfWeek.setter
	def FirstDayOfWeek(self, value): ...

	@property
	def FullDateTimePattern(self): ...

	@FullDateTimePattern.setter
	def FullDateTimePattern(self, value): ...

	def GetAbbreviatedDayName(self, _: System.DayOfWeek) -> str: ...
	def GetAbbreviatedEraName(self, _: int) -> str: ...
	def GetAbbreviatedMonthName(self, _: int) -> str: ...
	def GetAllDateTimePatterns(self, _: str) -> List[str]: ...
	def GetDayName(self, _: System.DayOfWeek) -> str: ...
	def GetEra(self, _: str) -> int: ...
	def GetEraName(self, _: int) -> str: ...
	def GetFormat(self, _: Type) -> object: ...
	def GetHashCode(self) -> int: ...
	def GetInstance(self, _: Any) -> DateTimeFormatInfo: ...
	def GetMonthName(self, _: int) -> str: ...
	def GetShortestDayName(self, _: System.DayOfWeek) -> str: ...
	def GetType(self) -> Type: ...
	def InvariantInfo(self, *args, **kwargs) -> Any: ...

	@property
	def IsReadOnly(self): ...

	@IsReadOnly.setter
	def IsReadOnly(self, value): ...

	@property
	def LongDatePattern(self): ...

	@LongDatePattern.setter
	def LongDatePattern(self, value): ...

	@property
	def LongTimePattern(self): ...

	@LongTimePattern.setter
	def LongTimePattern(self, value): ...

	def MemberwiseClone(self) -> object: ...

	@property
	def MonthDayPattern(self): ...

	@MonthDayPattern.setter
	def MonthDayPattern(self, value): ...

	@property
	def MonthGenitiveNames(self): ...

	@MonthGenitiveNames.setter
	def MonthGenitiveNames(self, value): ...

	@property
	def MonthNames(self): ...

	@MonthNames.setter
	def MonthNames(self, value): ...

	@property
	def NativeCalendarName(self): ...

	@NativeCalendarName.setter
	def NativeCalendarName(self, value): ...

	def Overloads(self, *args, **kwargs) -> Any: ...

	@property
	def PMDesignator(self): ...

	@PMDesignator.setter
	def PMDesignator(self, value): ...

	@property
	def RFC1123Pattern(self): ...

	@RFC1123Pattern.setter
	def RFC1123Pattern(self, value): ...

	def ReadOnly(
			self,
			_: DateTimeFormatInfo,
			) -> DateTimeFormatInfo: ...

	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def SetAllDateTimePatterns(self, _: List[str], __: str) -> None: ...

	@property
	def ShortDatePattern(self): ...

	@ShortDatePattern.setter
	def ShortDatePattern(self, value): ...

	@property
	def ShortTimePattern(self): ...

	@ShortTimePattern.setter
	def ShortTimePattern(self, value): ...

	@property
	def ShortestDayNames(self): ...

	@ShortestDayNames.setter
	def ShortestDayNames(self, value): ...

	@property
	def SortableDateTimePattern(self): ...

	@SortableDateTimePattern.setter
	def SortableDateTimePattern(self, value): ...

	@property
	def TimeSeparator(self): ...

	@TimeSeparator.setter
	def TimeSeparator(self, value): ...

	def ToString(self) -> str: ...

	@property
	def UniversalSortableDateTimePattern(self): ...

	@UniversalSortableDateTimePattern.setter
	def UniversalSortableDateTimePattern(self, value): ...

	@property
	def YearMonthPattern(self): ...

	@YearMonthPattern.setter
	def YearMonthPattern(self, value): ...

	def get_AMDesignator(self) -> str: ...
	def get_AbbreviatedDayNames(self) -> List[str]: ...
	def get_AbbreviatedMonthGenitiveNames(self) -> List[str]: ...
	def get_AbbreviatedMonthNames(self) -> List[str]: ...
	def get_Calendar(self) -> Calendar: ...
	def get_CalendarWeekRule(self) -> CalendarWeekRule: ...
	def get_CurrentInfo(self) -> DateTimeFormatInfo: ...
	def get_DateSeparator(self) -> str: ...
	def get_DayNames(self) -> List[str]: ...
	def get_FirstDayOfWeek(self) -> System.DayOfWeek: ...
	def get_FullDateTimePattern(self) -> str: ...
	def get_InvariantInfo(self) -> DateTimeFormatInfo: ...
	def get_IsReadOnly(self) -> bool: ...
	def get_LongDatePattern(self) -> str: ...
	def get_LongTimePattern(self) -> str: ...
	def get_MonthDayPattern(self) -> str: ...
	def get_MonthGenitiveNames(self) -> List[str]: ...
	def get_MonthNames(self) -> List[str]: ...
	def get_NativeCalendarName(self) -> str: ...
	def get_PMDesignator(self) -> str: ...
	def get_RFC1123Pattern(self) -> str: ...
	def get_ShortDatePattern(self) -> str: ...
	def get_ShortTimePattern(self) -> str: ...
	def get_ShortestDayNames(self) -> List[str]: ...
	def get_SortableDateTimePattern(self) -> str: ...
	def get_TimeSeparator(self) -> str: ...
	def get_UniversalSortableDateTimePattern(self) -> str: ...
	def get_YearMonthPattern(self) -> str: ...
	def set_AMDesignator(self, _: str) -> None: ...
	def set_AbbreviatedDayNames(self, _: List[str]) -> None: ...
	def set_AbbreviatedMonthGenitiveNames(self, _: List[str]) -> None: ...
	def set_AbbreviatedMonthNames(self, _: List[str]) -> None: ...
	def set_Calendar(self, _: Calendar) -> None: ...
	def set_CalendarWeekRule(self, _: CalendarWeekRule) -> None: ...
	def set_DateSeparator(self, _: str) -> None: ...
	def set_DayNames(self, _: List[str]) -> None: ...
	def set_FirstDayOfWeek(self, _: System.DayOfWeek) -> None: ...
	def set_FullDateTimePattern(self, _: str) -> None: ...
	def set_LongDatePattern(self, _: str) -> None: ...
	def set_LongTimePattern(self, _: str) -> None: ...
	def set_MonthDayPattern(self, _: str) -> None: ...
	def set_MonthGenitiveNames(self, _: List[str]) -> None: ...
	def set_MonthNames(self, _: List[str]) -> None: ...
	def set_PMDesignator(self, _: str) -> None: ...
	def set_ShortDatePattern(self, _: str) -> None: ...
	def set_ShortTimePattern(self, _: str) -> None: ...
	def set_ShortestDayNames(self, _: List[str]) -> None: ...
	def set_TimeSeparator(self, _: str) -> None: ...
	def set_YearMonthPattern(self, _: str) -> None: ...

class NumberFormatInfo:
	def __init__(self, *args, **kwargs) -> Any: ...
	def Clone(self) -> object: ...

	@property
	def CurrencyDecimalDigits(self): ...

	@CurrencyDecimalDigits.setter
	def CurrencyDecimalDigits(self, value): ...

	@property
	def CurrencyDecimalSeparator(self): ...

	@CurrencyDecimalSeparator.setter
	def CurrencyDecimalSeparator(self, value): ...

	@property
	def CurrencyGroupSeparator(self): ...

	@CurrencyGroupSeparator.setter
	def CurrencyGroupSeparator(self, value): ...

	@property
	def CurrencyGroupSizes(self): ...

	@CurrencyGroupSizes.setter
	def CurrencyGroupSizes(self, value): ...

	@property
	def CurrencyNegativePattern(self): ...

	@CurrencyNegativePattern.setter
	def CurrencyNegativePattern(self, value): ...

	@property
	def CurrencyPositivePattern(self): ...

	@CurrencyPositivePattern.setter
	def CurrencyPositivePattern(self, value): ...

	@property
	def CurrencySymbol(self): ...

	@CurrencySymbol.setter
	def CurrencySymbol(self, value): ...

	def CurrentInfo(self, *args, **kwargs) -> Any: ...

	@property
	def DigitSubstitution(self): ...

	@DigitSubstitution.setter
	def DigitSubstitution(self, value): ...

	def Equals(self, _: object, __: object) -> bool: ...
	def Finalize(self) -> None: ...
	def GetFormat(self, _: Type) -> object: ...
	def GetHashCode(self) -> int: ...
	def GetInstance(self, _: Any) -> NumberFormatInfo: ...
	def GetType(self) -> Type: ...
	def InvariantInfo(self, *args, **kwargs) -> Any: ...

	@property
	def IsReadOnly(self): ...

	@IsReadOnly.setter
	def IsReadOnly(self, value): ...

	def MemberwiseClone(self) -> object: ...

	@property
	def NaNSymbol(self): ...

	@NaNSymbol.setter
	def NaNSymbol(self, value): ...

	@property
	def NativeDigits(self): ...

	@NativeDigits.setter
	def NativeDigits(self, value): ...

	@property
	def NegativeInfinitySymbol(self): ...

	@NegativeInfinitySymbol.setter
	def NegativeInfinitySymbol(self, value): ...

	@property
	def NegativeSign(self): ...

	@NegativeSign.setter
	def NegativeSign(self, value): ...

	@property
	def NumberDecimalDigits(self): ...

	@NumberDecimalDigits.setter
	def NumberDecimalDigits(self, value): ...

	@property
	def NumberDecimalSeparator(self): ...

	@NumberDecimalSeparator.setter
	def NumberDecimalSeparator(self, value): ...

	@property
	def NumberGroupSeparator(self): ...

	@NumberGroupSeparator.setter
	def NumberGroupSeparator(self, value): ...

	@property
	def NumberGroupSizes(self): ...

	@NumberGroupSizes.setter
	def NumberGroupSizes(self, value): ...

	@property
	def NumberNegativePattern(self): ...

	@NumberNegativePattern.setter
	def NumberNegativePattern(self, value): ...

	def Overloads(self, *args, **kwargs) -> Any: ...

	@property
	def PerMilleSymbol(self): ...

	@PerMilleSymbol.setter
	def PerMilleSymbol(self, value): ...

	@property
	def PercentDecimalDigits(self): ...

	@PercentDecimalDigits.setter
	def PercentDecimalDigits(self, value): ...

	@property
	def PercentDecimalSeparator(self): ...

	@PercentDecimalSeparator.setter
	def PercentDecimalSeparator(self, value): ...

	@property
	def PercentGroupSeparator(self): ...

	@PercentGroupSeparator.setter
	def PercentGroupSeparator(self, value): ...

	@property
	def PercentGroupSizes(self): ...

	@PercentGroupSizes.setter
	def PercentGroupSizes(self, value): ...

	@property
	def PercentNegativePattern(self): ...

	@PercentNegativePattern.setter
	def PercentNegativePattern(self, value): ...

	@property
	def PercentPositivePattern(self): ...

	@PercentPositivePattern.setter
	def PercentPositivePattern(self, value): ...

	@property
	def PercentSymbol(self): ...

	@PercentSymbol.setter
	def PercentSymbol(self, value): ...

	@property
	def PositiveInfinitySymbol(self): ...

	@PositiveInfinitySymbol.setter
	def PositiveInfinitySymbol(self, value): ...

	@property
	def PositiveSign(self): ...

	@PositiveSign.setter
	def PositiveSign(self, value): ...

	def ReadOnly(
			self,
			_: NumberFormatInfo,
			) -> NumberFormatInfo: ...

	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def ToString(self) -> str: ...
	def get_CurrencyDecimalDigits(self) -> int: ...
	def get_CurrencyDecimalSeparator(self) -> str: ...
	def get_CurrencyGroupSeparator(self) -> str: ...
	def get_CurrencyGroupSizes(self) -> List[int]: ...
	def get_CurrencyNegativePattern(self) -> int: ...
	def get_CurrencyPositivePattern(self) -> int: ...
	def get_CurrencySymbol(self) -> str: ...
	def get_CurrentInfo(self) -> NumberFormatInfo: ...
	def get_DigitSubstitution(self) -> DigitShapes: ...
	def get_InvariantInfo(self) -> NumberFormatInfo: ...
	def get_IsReadOnly(self) -> bool: ...
	def get_NaNSymbol(self) -> str: ...
	def get_NativeDigits(self) -> List[str]: ...
	def get_NegativeInfinitySymbol(self) -> str: ...
	def get_NegativeSign(self) -> str: ...
	def get_NumberDecimalDigits(self) -> int: ...
	def get_NumberDecimalSeparator(self) -> str: ...
	def get_NumberGroupSeparator(self) -> str: ...
	def get_NumberGroupSizes(self) -> List[int]: ...
	def get_NumberNegativePattern(self) -> int: ...
	def get_PerMilleSymbol(self) -> str: ...
	def get_PercentDecimalDigits(self) -> int: ...
	def get_PercentDecimalSeparator(self) -> str: ...
	def get_PercentGroupSeparator(self) -> str: ...
	def get_PercentGroupSizes(self) -> List[int]: ...
	def get_PercentNegativePattern(self) -> int: ...
	def get_PercentPositivePattern(self) -> int: ...
	def get_PercentSymbol(self) -> str: ...
	def get_PositiveInfinitySymbol(self) -> str: ...
	def get_PositiveSign(self) -> str: ...
	def set_CurrencyDecimalDigits(self, _: int) -> None: ...
	def set_CurrencyDecimalSeparator(self, _: str) -> None: ...
	def set_CurrencyGroupSeparator(self, _: str) -> None: ...
	def set_CurrencyGroupSizes(self, _: List[int]) -> None: ...
	def set_CurrencyNegativePattern(self, _: int) -> None: ...
	def set_CurrencyPositivePattern(self, _: int) -> None: ...
	def set_CurrencySymbol(self, _: str) -> None: ...
	def set_DigitSubstitution(self, _: DigitShapes) -> None: ...
	def set_NaNSymbol(self, _: str) -> None: ...
	def set_NativeDigits(self, _: List[str]) -> None: ...
	def set_NegativeInfinitySymbol(self, _: str) -> None: ...
	def set_NegativeSign(self, _: str) -> None: ...
	def set_NumberDecimalDigits(self, _: int) -> None: ...
	def set_NumberDecimalSeparator(self, _: str) -> None: ...
	def set_NumberGroupSeparator(self, _: str) -> None: ...
	def set_NumberGroupSizes(self, _: List[int]) -> None: ...
	def set_NumberNegativePattern(self, _: int) -> None: ...
	def set_PerMilleSymbol(self, _: str) -> None: ...
	def set_PercentDecimalDigits(self, _: int) -> None: ...
	def set_PercentDecimalSeparator(self, _: str) -> None: ...
	def set_PercentGroupSeparator(self, _: str) -> None: ...
	def set_PercentGroupSizes(self, _: List[int]) -> None: ...
	def set_PercentNegativePattern(self, _: int) -> None: ...
	def set_PercentPositivePattern(self, _: int) -> None: ...
	def set_PercentSymbol(self, _: str) -> None: ...
	def set_PositiveInfinitySymbol(self, _: str) -> None: ...
	def set_PositiveSign(self, _: str) -> None: ...

class DateTimeStyles:
	def __init__(self, *args, **kwargs) -> Any: ...
	def AdjustToUniversal(self, *args, **kwargs) -> Any: ...
	def AllowInnerWhite(self, *args, **kwargs) -> Any: ...
	def AllowLeadingWhite(self, *args, **kwargs) -> Any: ...
	def AllowTrailingWhite(self, *args, **kwargs) -> Any: ...
	def AllowWhiteSpaces(self, *args, **kwargs) -> Any: ...
	def AssumeLocal(self, *args, **kwargs) -> Any: ...
	def AssumeUniversal(self, *args, **kwargs) -> Any: ...
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
	def NoCurrentDateDefault(self, *args, **kwargs) -> Any: ...
	def Overloads(self, *args, **kwargs) -> Any: ...
	def Parse(self, _: Type, __: str, ___: bool) -> object: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def RoundtripKind(self, *args, **kwargs) -> Any: ...
	def ToObject(self, _: Type, __: object) -> object: ...
	def ToString(self, _: str, __: Any) -> str: ...
	def TryParse(self, *args, **kwargs) -> Any: ...

class DigitShapes:
	def __init__(self, *args, **kwargs) -> Any: ...
	def CompareTo(self, _: object) -> int: ...
	def Context(self, *args, **kwargs) -> Any: ...
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
	def NativeNational(self, *args, **kwargs) -> Any: ...
	def Overloads(self, *args, **kwargs) -> Any: ...
	def Parse(self, _: Type, __: str, ___: bool) -> object: ...
	def ReferenceEquals(self, _: object, __: object) -> bool: ...
	def ToObject(self, _: Type, __: object) -> object: ...
	def ToString(self, _: str, __: Any) -> str: ...
	def TryParse(self, *args, **kwargs) -> Any: ...

class TimeSpanStyles:
	def __init__(self, *args, **kwargs) -> Any: ...
	def AssumeNegative(self, *args, **kwargs) -> Any: ...
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