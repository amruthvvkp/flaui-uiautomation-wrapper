Feature: WPF simple controls
  As a FlaUI for Python user
  I want to automate the bundled WPF test application
  So that I can verify common control interactions in plain language

  Scenario: The application launches with the expected title
    Given the WPF test application is running
    Then the window title is "FlaUI WPF Test App"

  Scenario: Enter text into the text box
    Given the WPF test application is running
    When I enter "hello from behave" into the text box
    Then the text box contains "hello from behave"

  Scenario: Toggle the test checkbox
    Given the WPF test application is running
    When I toggle the test checkbox
    Then the test checkbox state is inverted
