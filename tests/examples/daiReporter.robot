*** Settings ***
Library    ../../resources/daiMobileLibrary.py

Resource    ../../resources/cloudCredentialsLOCAL.robot
Resource    ../../steps/stepsExperiBank.robot


Suite Setup  	Perform Suite Setup Actions    suiteName=CT Features Example    with_unique_stamp=True    # other appium capabilities can be added here as kwargs
Suite Teardown	Perform Suite Teardown Actions

Test Setup  	Perform Test Setup Actions    with_app_activation=True
Test Teardown   Perform Test Teardown Actions

*** Test Cases ***
01.DigitalAI sunny
    Report    message=some message    status=${True}
    Get Test Property    property_name=reportUrl

02.DigitalAI rainy
    Wait Until Page Contains Element    xpath=//*[@text='Username']
    Wait Until Element Is Visible       xpath=//*[@text='Username']
    Click Element                       id=com.experitest.ExperiBank:id/loginButton
    Wait Until Page Contains Element    xpath=//*[@text='Username1']

03.DigitalAI with gherkin
    Given Login to ExperiBank app
    When Send payment in ExperiBank app
    And Confirm payment in ExperiBank app
    Then Logout from ExperiBank app

04.DigitalAI ExperiBank login - data from excel
    [Tags]    excel-data
    Login to Experibank using excel    file_path=tests/examples/data.xlsx
