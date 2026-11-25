# Unittest Example

A complete, runnable `unittest` suite lives in the repository at
[`examples/unittest/`](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/tree/master/examples/unittest).
It uses only the standard library and automates the bundled WPF test application, so there is
nothing extra to install.

## Run it

```bash
uv run python -m unittest discover -s examples/unittest -v
```

## The suite

`setUpClass` launches the application once for the class and `tearDownClass` disposes it, the
`unittest` equivalent of the session fixture in the [pytest example](pytest.md). Tests that change
shared state undo it with `addCleanup`. The C# tab shows the same suite in NUnit, the framework
FlaUI's own UI tests use.

=== "Python"

    ```python
    --8<-- "examples/unittest/test_simple_controls.py"
    ```

=== "C# (NUnit)"

    ```csharp
    using FlaUI.Core;
    using FlaUI.Core.AutomationElements;
    using FlaUI.Core.Definitions;
    using FlaUI.Core.Tools;
    using FlaUI.UIA3;
    using NUnit.Framework;

    [TestFixture]
    public class SimpleControlsTest
    {
        private UIA3Automation _automation;
        private Application _app;
        private Window _window;
        private ConditionFactory _cf;

        [OneTimeSetUp]
        public void SetUpClass()
        {
            _automation = new UIA3Automation();
            _app = Application.Launch(TestApp.Path);
            _window = _app.GetMainWindow(_automation);
            _cf = _automation.ConditionFactory;
        }

        [OneTimeTearDown]
        public void TearDownClass()
        {
            _app.Kill();
            _automation.Dispose();
        }

        [Test]
        public void WindowTitle() => Assert.That(_window.Title, Is.EqualTo("FlaUI WPF Test App"));

        [Test]
        public void EnterText()
        {
            var textBox = _window.FindFirstDescendant(_cf.ByAutomationId("TextBox")).AsTextBox();
            textBox.Text = "hello from NUnit";
            Assert.That(textBox.Text, Is.EqualTo("hello from NUnit"));
        }

        [Test]
        public void InvokeButton()
        {
            var button = _window.FindFirstDescendant(_cf.ByAutomationId("InvokableButton")).AsButton();
            button.Invoke();
            Assert.That(Retry.WhileFalse(() => button.Name == "Invoked!", TimeSpan.FromSeconds(2)).Result);
        }

        [Test]
        public void ToggleCheckbox()
        {
            var checkBox = _window.FindFirstDescendant(_cf.ByName("Test Checkbox")).AsCheckBox();
            var original = checkBox.ToggleState;
            checkBox.Toggle();
            try { Assert.That(checkBox.ToggleState, Is.Not.EqualTo(original)); }
            finally { if (checkBox.ToggleState != original) checkBox.Toggle(); }
        }
    }
    ```
