class Application:
    def __init__(self, application) -> None:
        self.application = application

    def attach(self, *args):
        """Attach
        Attach


        :param: args: Generic FlaUI Element
        """
        return self.application.Attach(self, *args)


    def attach_or_launch(self, *args):
        """AttachOrLaunch
        AttachOrLaunch


        :param: args: Generic FlaUI Element
        """
        return self.application.AttachOrLaunch(self, *args)


    def close(self, *args):
        """Close
        Close


        :param: args: Generic FlaUI Element
        """
        return self.application.Close(self, *args)


    def close_timeout(self, *args):
        """CloseTimeout
        CloseTimeout


        :param: args: Generic FlaUI Element
        """
        return self.application.CloseTimeout(self, *args)


    def dispose(self, *args):
        """Dispose
        Dispose


        :param: args: Generic FlaUI Element
        """
        return self.application.Dispose(self, *args)


    def equals(self, *args):
        """Equals
        Equals


        :param: args: Generic FlaUI Element
        """
        return self.application.Equals(self, *args)


    def exit_code(self, *args):
        """ExitCode
        ExitCode


        :param: args: Generic FlaUI Element
        """
        return self.application.ExitCode(self, *args)


    def finalize(self, *args):
        """Finalize
        Finalize


        :param: args: Generic FlaUI Element
        """
        return self.application.Finalize(self, *args)


    def get_all_top_level_windows(self, *args):
        """GetAllTopLevelWindows
        GetAllTopLevelWindows


        :param: args: Generic FlaUI Element
        """
        return self.application.GetAllTopLevelWindows(self, *args)


    def get_hash_code(self, *args):
        """GetHashCode
        GetHashCode


        :param: args: Generic FlaUI Element
        """
        return self.application.GetHashCode(self, *args)


    def get_main_window(self, *args):
        """GetMainWindow
        GetMainWindow


        :param: args: Generic FlaUI Element
        """
        return self.application.GetMainWindow(self, *args)


    def get_type(self, *args):
        """GetType
        GetType


        :param: args: Generic FlaUI Element
        """
        return self.application.GetType(self, *args)


    def has_exited(self, *args):
        """HasExited
        HasExited


        :param: args: Generic FlaUI Element
        """
        return self.application.HasExited(self, *args)


    def is_store_app(self, *args):
        """IsStoreApp
        IsStoreApp


        :param: args: Generic FlaUI Element
        """
        return self.application.IsStoreApp(self, *args)


    def kill(self, *args):
        """Kill
        Kill


        :param: args: Generic FlaUI Element
        """
        return self.application.Kill(self, *args)


    def launch(self, *args):
        """Launch
        Launch


        :param: args: Generic FlaUI Element
        """
        return self.application.Launch(self, *args)


    def launch_store_app(self, *args):
        """LaunchStoreApp
        LaunchStoreApp


        :param: args: Generic FlaUI Element
        """
        return self.application.LaunchStoreApp(self, *args)


    def main_window_handle(self, *args):
        """MainWindowHandle
        MainWindowHandle


        :param: args: Generic FlaUI Element
        """
        return self.application.MainWindowHandle(self, *args)


    def memberwise_clone(self, *args):
        """MemberwiseClone
        MemberwiseClone


        :param: args: Generic FlaUI Element
        """
        return self.application.MemberwiseClone(self, *args)


    def name(self, *args):
        """Name
        Name


        :param: args: Generic FlaUI Element
        """
        return self.application.Name(self, *args)


    def overloads(self, *args):
        """Overloads
        Overloads


        :param: args: Generic FlaUI Element
        """
        return self.application.Overloads(self, *args)


    def process_id(self, *args):
        """ProcessId
        ProcessId


        :param: args: Generic FlaUI Element
        """
        return self.application.ProcessId(self, *args)


    def reference_equals(self, *args):
        """ReferenceEquals
        ReferenceEquals


        :param: args: Generic FlaUI Element
        """
        return self.application.ReferenceEquals(self, *args)


    def to_string(self, *args):
        """ToString
        ToString


        :param: args: Generic FlaUI Element
        """
        return self.application.ToString(self, *args)


    def wait_while_busy(self, *args):
        """WaitWhileBusy
        WaitWhileBusy


        :param: args: Generic FlaUI Element
        """
        return self.application.WaitWhileBusy(self, *args)


    def wait_while_main_handle_is_missing(self, *args):
        """WaitWhileMainHandleIsMissing
        WaitWhileMainHandleIsMissing


        :param: args: Generic FlaUI Element
        """
        return self.application.WaitWhileMainHandleIsMissing(self, *args)
