"""Auto-Generated wrapper for Application from the <class 'FlaUI.Core.Application'> from the module - FlaUI.Core/nVoid .ctor(System.Diagnostics.Process, Boolean)
Void .ctor(Int32, Boolean)"""
from FlaUI.Core import Application
class Application:
	def __init__(self):
		self.application = Application
		self.name = self.application.Name		self.process_id = self.application.ProcessId		self.is_store_app = self.application.IsStoreApp		self.close_timeout = self.application.CloseTimeout		self.has_exited = self.application.HasExited		self.main_window_handle = self.application.MainWindowHandle		self.exit_code = self.application.ExitCode
	def launch(self):		return self.application.Launch()
	def get_all_top_level_windows(self):		return self.application.GetAllTopLevelWindows()
	def launch_store_app(self):		return self.application.LaunchStoreApp()
	def get_main_window(self):		return self.application.GetMainWindow()
	def attach(self):		return self.application.Attach()
	def attach_or_launch(self):		return self.application.AttachOrLaunch()
	def kill(self):		return self.application.Kill()
	def dispose(self):		return self.application.Dispose()
	def close(self):		return self.application.Close()
	def wait_while_main_handle_is_missing(self):		return self.application.WaitWhileMainHandleIsMissing()
	def wait_while_busy(self):		return self.application.WaitWhileBusy()
