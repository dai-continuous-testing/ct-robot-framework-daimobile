*** Settings ***
Library    ExcellentLibrary
Library    ../resources/daiMobileLibrary.py

*** Comments ***
This file contains top level steps (keywords) that are later translated into RobotFramework keywords.
Those top level keywords intent to describe business logic. 

*** Keywords ***
Login to ExperiBank app
    [Setup]    Start Group
    Portrait                                                                        
	Input Text	        xpath=//*[@text='Username']	    company                                 
	Input Text	        xpath=//*[@text='Password']	    company
	Click Element	    xpath=//*[@resource-id='com.experitest.ExperiBank:id/loginButton']      
	BuiltIn.Sleep	    5s
    [Teardown]    Stop Group    

Send payment in ExperiBank app
    [Setup]    Start Group
    Click Element	    id=com.experitest.ExperiBank:id/makePaymentButton
	Input Text	        id=com.experitest.ExperiBank:id/phoneTextField		0501234567
	Input Text	        id=com.experitest.ExperiBank:id/nameTextField		John Snow
	Input Text	        id=com.experitest.ExperiBank:id/amountTextField		50
	Input Text	        id=com.experitest.ExperiBank:id/countryTextField	Switzerland
	Click Element	    id=com.experitest.ExperiBank:id/sendPaymentButton
    [Teardown]    Stop Group

Confirm payment in ExperiBank app
    [Setup]    Start Group
    Click Element	    id=android:id/button1
    [Teardown]    Stop Group

Logout from ExperiBank app
    [Setup]    Start Group
	Click Element	    xpath=//*[@text='Logout']
    [Teardown]    Stop Group

Login with invalid credentials to ExperiBank app
    [Setup]    Start Group
    Portrait                                                                        
	Input Text	        xpath=//*[@text='Username']	wrong                                 
	Input Text	        xpath=//*[@text='Password']	wrong
	Click Element	    xpath=//*[@resource-id='com.experitest.ExperiBank:id/loginButton']      
	BuiltIn.Sleep	    5s
    Wait Until Page Contains Element   //*[@text='Close']
    [Teardown]    Stop Group

Login to ExperiBank with credentials
    [Arguments]    ${usr}    ${pas}
    [Setup]    Start Steps Group    data driven test > login to experibank with credentials | user= ${usr} | password= ${pas}
        Start Application
        Portrait                                                                        
        Run Keyword If      '${usr}' != 'None'    Input Text    xpath=//*[@text='Username']	${usr}                           
        Run Keyword If      '${pas}' != 'None'   Input Text    xpath=//*[@text='Password']	${pas}
        Click Element	    xpath=//*[@resource-id='com.experitest.ExperiBank:id/loginButton']      
        BuiltIn.Sleep	    5s
        Stop Application
    [Teardown]    Stop Group

Login to Experibank using excel
    [Arguments]    ${file_path}    ${get_column_names}=true
    Open Workbook    file_path=${file_path}
    @{data}=    Read Sheet Data    get_column_names_from_header_row=${get_column_names} 
    FOR  ${row}  IN  @{data}
        Login to ExperiBank with credentials    ${row}[username]    ${row}[password]
    END
