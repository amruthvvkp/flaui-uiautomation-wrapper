# flaui-uiautomation-wrapper

[![GitHub contributors](https://img.shields.io/github/contributors/amruthvvkp/flaui-uiautomation-wrapper)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/graphs/contributors)
[![GitHub license](https://img.shields.io/github/license/amruthvvkp/flaui-uiautomation-wrapper)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/blob/master/LICENSE)
![GitHub branch checks state](https://img.shields.io/github/checks-status/amruthvvkp/flaui-uiautomation-wrapper/master)
![GitHub language count](https://img.shields.io/github/languages/count/amruthvvkp/flaui-uiautomation-wrapper)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/amruthvvkp/flaui-uiautomation-wrapper)
![GitHub last commit](https://img.shields.io/github/last-commit/amruthvvkp/flaui-uiautomation-wrapper)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flaui-uiautomation-wrapper)
![PyPI - Unsupported Versions](https://img.shields.io/badge/Python-3.9%20|%203.10%20Unsupported%20Python.Net%20Versions-yellowgreen)
![PyPI - Downloads](https://img.shields.io/pypi/dm/flaui-uiautomation-wrapper)

[![Python package](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/actions/workflows/python-package.yml/badge.svg)](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/actions/workflows/python-package.yml)

![GitHub pull requests](https://img.shields.io/github/issues-pr/amruthvvkp/flaui-uiautomation-wrapper)
![GitHub milestones](https://img.shields.io/github/milestones/all/amruthvvkp/flaui-uiautomation-wrapper)

[FlaUI](https://github.com/FlaUI/FlaUI#:~:text=FlaUI%20is%20a%20.,of%20a%20wrapper%20around%20them.) is a .NET library that can be used to perform UI automated testing of Windows desktop applications like Win32, WinForms, WPF, etc.. It is a wrapper that works alongside Windows inbuilt UI Automation technology to perform UI automation as required.

FlaUI has interesting approaches on multiple non-python projects. On python there is an integration with RobotFramework which allows tests to be written on [RobotFramework](https://github.com/GDATASoftwareAG/robotframework-flaui) and the keywords from it's plugin are utilized to identify elements by XPATH and perform UI actions.

Other than RobotFramework-FLAUI, there are no Python libraries that help us leverage this useful C# library. The intend of this project is to make sure that a versatile and useful plug-and-play python wrapper is built which works well with IDE's intellisense, integrating with any Python frameworks like [PyTest](https://docs.pytest.org/en/7.1.x/), [Behave](https://behave.readthedocs.io/en/stable/), [TestPlan](https://github.com/morganstanley/testplan), etc. or any other tooling where UI automation is a necessary feature.

This project is in active development over the latest version of FlaUI (3.2.0) available on GitHub. New releases are expected to come by in the next few weeks and certainly the documentation would improve alongside the planned releases.

If you would like to contribute or request a feature, feel free to join the discussions on the [project's GitHub page](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/discussions).

This project is designed to work only on Python 3.7 or 3.8 due to the Python version dependency from Pythonnet 2.5.2, PythonNet 3.0.0 is under development and post it's release this project would support Python 3.9 & 3.10.

## Release Notes

Check out the release notes on [GitHub releases](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/releases).
