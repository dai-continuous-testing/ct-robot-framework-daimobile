*** Settings ***
Library    AppiumLibrary

Resource    ../../resources/cloudCredentialsLOCAL.robot

Suite Setup  	Start Session    Example Robot Framework | Before
Suite Teardown	Close Application

*** Comments ***
Example tests for Experibank app.
Designed to trigger on Android, go to /capabilities/deviceCapabilities.robot to set the platform

*** Variables ***
${APPIUM_VERSION}        2.2.2
${PLATFORM_NAME}         android
${DEVICE_QUERY}          @os='${PLATFORM_NAME}' and @category='PHONE'

# Android specific
${ANDROID_PACKAGE}       com.experitest.ExperiBank
${ANDROID_ACTIVITY}      .LoginActivity

*** Keywords ***
Start Session
    [Arguments]   ${SUITE_NAME}
    Open Application
        ...			${cloudUrl}	digitalai:accessKey=${accessKey}
        ...			app=cloud:${ANDROID_PACKAGE}/${ANDROID_ACTIVITY}
        ...			platformName=${PLATFORM_NAME}	
        ...         appPackage=${ANDROID_PACKAGE}
        ...			appActivity=${ANDROID_ACTIVITY}
        ...         appiumVersion=${APPIUM_VERSION}
        ...         testName=${SUITE_NAME} 
        ...         deviceQuery=${DEVICE_QUERY}

*** Test Cases ***
Login and perform payment
	Portrait                                                                        
	AppiumLibrary.Input Text	        xpath=//*[@text='Username']	company                                 
	AppiumLibrary.Input Text	        xpath=//*[@text='Password']	company
	AppiumLibrary.Click Element	    xpath=//*[@resource-id='com.experitest.ExperiBank:id/loginButton']      
	BuiltIn.Sleep	    5s
	AppiumLibrary.Click Element	    id=com.experitest.ExperiBank:id/makePaymentButton
	AppiumLibrary.Input Text	        id=com.experitest.ExperiBank:id/phoneTextField		0501234567
	AppiumLibrary.Input Text	        id=com.experitest.ExperiBank:id/nameTextField		John Snow
	AppiumLibrary.Input Text	        id=com.experitest.ExperiBank:id/amountTextField		50
	AppiumLibrary.Input Text	        id=com.experitest.ExperiBank:id/countryTextField	Switzerland
	AppiumLibrary.Click Element	    id=com.experitest.ExperiBank:id/sendPaymentButton
	AppiumLibrary.Click Element	    id=android:id/button1
	AppiumLibrary.Click Element	    xpath=//*[@text='Logout']

Invalid login
	AppiumLibrary.Input Text	        xpath=//*[@text='Username']    wrong
	AppiumLibrary.Input Text	        xpath=//*[@text='Password']    company
	AppiumLibrary.Click Element    	id=com.experitest.ExperiBank:id/loginButton
	AppiumLibrary.Wait Until Page Contains Element    //*[@text='_INVALID_TO_FAIL_THE_TEST']
