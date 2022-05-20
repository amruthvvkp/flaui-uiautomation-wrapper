# flaui-uiautomation-wrapper

[FlaUI](https://github.com/FlaUI/FlaUI#:~:text=FlaUI%20is%20a%20.,of%20a%20wrapper%20around%20them.) is a .NET library that can be used to perform UI automated testing of Windows desktop applications like Win32, WinForms, WPF, etc.. It is a wrapper that works alongside Windows inbuilt UI Automation technology to perform UI automation as required.

FlaUI has interesting approaches on multiple non-python projects. On python there is an integration with RobotFramework which allows tests to be written on [RobotFramework](https://github.com/GDATASoftwareAG/robotframework-flaui) and the keywords from it's plugin are utilized to identify elements by XPATH and perform UI actions.

Other than RobotFramework-FLAUI, there are no Python libraries that help us leverage this useful C# library. The intend of this project is to make sure that a versatile and useful plug-and-play python wrapper is built which works well with IDE's intellisense, integrating with any Python frameworks like [PyTest](https://docs.pytest.org/en/7.1.x/), [Behave](https://behave.readthedocs.io/en/stable/), [TestPlan](https://github.com/morganstanley/testplan), etc. or any other tooling where UI automation is a necessary feature.

This project is in active development over the latest version of FlaUI (3.2.0) available on GitHub. New releases are expected to come by in the next few weeks and certainly the documentation would improve alongside the planned releases.

If you would like to contribute or request a feature, feel free to join the discussions on the [project's GitHub page](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/discussions).