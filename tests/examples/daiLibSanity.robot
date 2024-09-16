*** Settings ***
Library    ../../resources/daiMobileLibrary.py

Resource    ../../resources/cloudCredentialsLOCAL.robot
Resource    ../../steps/stepsExperiBank.robot


Suite Setup  	Perform Suite Setup Actions    suiteName=Lib Sanity    with_unique_stamp=True
Suite Teardown	Perform Suite Teardown Actions

Test Setup  	Perform Test Setup Actions    with_app_activation=True
Test Teardown   Perform Test Teardown Actions

*** Test Cases ***
01.DigitalAI Lib Sanity
    Get Test Property    property_name=udid
    Input Text    USERNAME_INPUT    some message
    Clear Text    USERNAME_INPUT
    Input Text    USERNAME_INPUT    company
    Input Password   PASSWORD_INPUT    company
    Click Element    LOGIN_BUTTON
    Sleep    5s    feature testing
    Page Should Contain Element    MAKE_PAYMENT_BUTTON
    Click Element    LOGOUT_BUTTON
