# Test applications

We intend to use a WPF application for UIA3 and a WinForms application for UIA2 automated testing. These application sources are available under FlaUI GitHub repository - `src\TestApplications`

## Getting Started

Ideally we would like to run a pre-baked PowerShell script from the FlaUI GitHub repository. This script will download the latest version of the test applications and build them. The script will also download the latest version of the FlaUI binaries and place them in the test applications' bin folder.

## Building the test applications

### Download FlaUI repository from GitHub

We need to download the FlaUI repository from GitHub. This can be done using the following command:

```powershell
git clone https://github.com/FlaUI/FlaUI.git
```

### Build the test applications

FlaUI repository has a PowerShell script builds the required applications. This can be found at - `build.ps1`

```powershell
cd .\FlaUI # Navigating to the cloned FlaUI repository
.\build.ps1
```

### Move the binaries to the test applications' bin folder

The FlaUI repository would contain executables for the test applications. These executables need to be moved to the test applications' bin folder. This can be done using the following command:

```powershell
cd flaui-uiautomation-wrapper # Navigate to this project root folder
mkdir test_applications # Create a test_applications folder
cd test_applications # Navigate to the test_applications folder
mkdir WPFApplication # Create a WPFApplication folder
mkdir WinFormsApplication # Create a WinFormsApplication folder

# Assign current directory to a variable
$testApplicationsPath = (Get-Location).Path

cd .\FlaUI\src\TestApplications # Navigating to the test applications folder under FlaUI repository
cp .\WpfApplication\bin\* $testApplicationsPath\WPFApplication # Copying the WPF application binaries to the test applications' bin folder
cp .\WinFormsApplication\bin\* $testApplicationsPath\WinFormsApplication # Copying the WinForms application binaries to the test applications' bin folder
```

## Running Unit Tests/Integration Tests on the copied test applications

Use the below table to find the test executable for the respective UIAutomation version.
| UIAutomation | Test Executable |
| ------------ | --------------------------------------------------------------- |
| UIA2 | `test_applications\WinFormsApplication\WinFormsApplication.exe` |
| UIA3 | `test_applications\WPFApplication\WpfApplication.exe` |
