*** Settings ***
Library    ../../resources/daiMobileLibrary.py

Resource    ../../resources/cloudCredentialsLOCAL.robot
Resource    ../../steps/stepsExperiBank.robot


Suite Setup  	Perform Suite Setup Actions    suiteName=CT Features Example    with_unique_stamp=True    newCommandTimeout=60
Suite Teardown	Perform Suite Teardown Actions

Test Setup  	Perform Test Setup Actions    with_app_activation=True
Test Teardown   Perform Test Teardown Actions

*** Test Cases ***
01.DigitalAI measure performance
    Portrait
    Add Test Property    key=cicd_example    value=true
    Start Performance Transaction
    Login to ExperiBank app
    End Performance Transaction    name=LoginExperiBank

02.DigitalAI voice assitant
    Portrait
    Activate Voice Assistance    open device settings
    Add Test Property    key=voiceAssistant    value=enabled
    
