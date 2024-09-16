*** Settings ***
Library    ../../resources/daiMobileLibrary.py

Resource    ../../resources/cloudCredentialsLOCAL.robot
Resource    ../../steps/stepsExperiBank.robot


Suite Setup  	Perform Suite Setup Actions    suiteName=Lib Sanity    with_unique_stamp=True    newCommandTimeout=60
Suite Teardown	Perform Suite Teardown Actions

Test Setup  	Perform Test Setup Actions    with_app_activation=True
Test Teardown   Perform Test Teardown Actions

*** Keywords ***
Run quick test
    Get Test Property    property_name=udid
    Wait Until Page Contains Element    xpath=//*[@text='Login']

*** Test Cases ***
01.DigitalAI Lib Sanity
    Run quick test

02.DigitalAI Lib Sanity
    Run quick test

03.DigitalAI Lib Sanity
    Run quick test

04.DigitalAI Lib Sanity
    Run quick test

05.DigitalAI Lib Sanity
    Run quick test

06.DigitalAI Lib Sanity
    Run quick test

07.DigitalAI Lib Sanity
    Run quick test

08.DigitalAI Lib Sanity
    Run quick test

09.DigitalAI Lib Sanity
    Run quick test

10.DigitalAI Lib Sanity
    Run quick test

11.DigitalAI Lib Sanity
    Run quick test

12.DigitalAI Lib Sanity
    Run quick test

13.DigitalAI Lib Sanity
    Run quick test

14.DigitalAI Lib Sanity
    Run quick test

15.DigitalAI Lib Sanity
    Run quick test

16.DigitalAI Lib Sanity
    Run quick test

17.DigitalAI Lib Sanity
    Run quick test

18.DigitalAI Lib Sanity
    Run quick test

19.DigitalAI Lib Sanity
    Run quick test

20.DigitalAI Lib Sanity
    Run quick test
