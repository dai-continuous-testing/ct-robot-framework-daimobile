*** Settings ***
Library    ../../resources/daiMobileLibrary.py

Resource    ../../resources/cloudCredentialsLOCAL.robot

Suite Setup  	Start Session    Example Robot Framework | After
Suite Teardown	Perform Suite Teardown Actions

Test Setup  	Perform Test Setup Actions
Test Teardown   Perform Test Teardown Actions

*** Comments ***
Example tests for Experibank app.
Designed to trigger on Android, go to /capabilities/deviceCapabilities.robot to set the platform

*** Test Cases ***
Login and perform payment
	Portrait                                                                        
	Input Text	        xpath=//*[@text='Username']	company                                 
	Input Text	        xpath=//*[@text='Password']	company
	Click Element	    xpath=//*[@resource-id='com.experitest.ExperiBank:id/loginButton']      
	BuiltIn.Sleep	    5s
	Click Element	    id=com.experitest.ExperiBank:id/makePaymentButton
	Input Text	        id=com.experitest.ExperiBank:id/phoneTextField		0501234567
	Input Text	        id=com.experitest.ExperiBank:id/nameTextField		John Snow
	Input Text	        id=com.experitest.ExperiBank:id/amountTextField		50
	Input Text	        id=com.experitest.ExperiBank:id/countryTextField	Switzerland
	Click Element	    id=com.experitest.ExperiBank:id/sendPaymentButton
	Click Element	    id=android:id/button1
	Click Element	    xpath=//*[@text='Logout']

Invalid login
	Input Text	        xpath=//*[@text='Username']    wrong
	Input Text	        xpath=//*[@text='Password']    company
	Click Element    	id=com.experitest.ExperiBank:id/loginButton
	Wait Until Page Contains Element    //*[@text='_INVALID_TO_FAIL_THE_TEST']    # error
