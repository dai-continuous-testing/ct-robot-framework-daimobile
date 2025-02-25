*** Settings ***
Library    ../../resources/daiMobileLibrary.py

Resource    ../../resources/cloudCredentials.robot
Resource    ../../steps/stepsExperiBank.robot


Suite Setup  	Perform Suite Setup Actions    suiteName=Time measurements    with_unique_stamp=True    newCommandTimeout=300    noReset=true
Suite Teardown	Perform Suite Teardown Actions

Test Setup  	Perform Test Setup Actions    with_app_activation=True
Test Teardown   Perform Test Teardown Actions

*** Keywords ***
Measure time
    [Arguments]    ${t}
    ${startTime}    Get Time
    Implicit Wait    time=${t}    reason=wait ${t} seconds
    ${endTime}    Get Time
    ${time}   Count Time Delta   ${startTime}    ${endTime}
    Report    message=Time elapsed: ${time}    status=${True}

*** Test Cases ***
Measure time of steps
    Measure time    10
    Measure time    30
    Measure time    60
    Measure time    120
