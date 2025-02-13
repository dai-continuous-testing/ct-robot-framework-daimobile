import os
import inspect
import traceback
from datetime import datetime

from AppiumLibrary import AppiumLibrary
from SeleniumLibrary import SeleniumLibrary
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
from functools import wraps

from timeouts import global_long_timeout, global_timeout
from capabilities.appiumCapabilities import *

from elementLocators.android_locators import android_locators
from elementLocators.ios_locators import ios_locators


log_level = "INFO"

def handle_exceptions(method):
                @wraps(method)
                def wrapper(*args, **kwargs):
                        self = args[0]  # Assuming the instance of daiMobileLibrary(AppiumLibrary) is the first argument
                        if isinstance(self, daiMobileLibrary):
                                error = None
                                method_name = method.__name__  # Get the name of the decorated method
                                try:
                                        log_lvl = self.build_in.get_variable_value('${LOG LEVEL}', log_level)
                                        signature = inspect.signature(method)
                                        parameters = list(signature.parameters.values())[1:]  # Skip the first parameter (self)
                                        # Construct the arguments string for logging
                                        arguments_str = ' | '.join(f"{param.name}={args[i + 1]}" for i, param in enumerate(parameters))
                                        method_name_str = str(method_name).replace("_", " ")
                                        if log_lvl == 'DEBUG':
                                                self.build_in.log_to_console("\nmethod: {}, args: {}".format(method_name, arguments_str))
                                        self.start_steps_group(name=f"{method_name_str} | {arguments_str}")
                                        method(*args, **kwargs)
                                except Exception as e:
                                        error = e
                                        if log_lvl == 'DEBUG':
                                                traceback_str = traceback.format_exc()
                                                self.build_in.log_to_console(traceback_str)
                                        self.build_in.fail("Exception: {}".format(error))
                                finally:
                                        # Assume we have a method called steps_group_action_teardown in daiMobileLibrary
                                        self.steps_group_action_teardown(error) 
                        else:
                                raise Exception("Problem with 'self' which is not of type 'daiMobileLibrary'")
                return wrapper


class daiMobileLibrary(AppiumLibrary):
        ROBOT_LISTENER_API_VERSION = 2
        ROBOT_LIBRARY_SCOPE = "GLOBAL"

        def __init__(self):
                super(daiMobileLibrary, self).__init__()
                self.ROBOT_LIBRARY_LISTENER = self
                self.keywords = []
                self.driver = None
                self.build_in = BuiltIn()
                self.failed_test_names = []
                self.test_results = []
                self.library_version = "1.3"
                self.unique_stamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        def _start_keyword(self, name, attrs):
                self.keywords.append(name)

        def _get_top_keyword_name(self, level=-2):
                return self.keywords[level].split(".")[-1]
        
        def start_session(self, suite_name, **kwargs):
                cloudUrl = self.build_in.get_variable_value("${cloudUrl}")
                accessKeyEnvVarName = self.build_in.get_variable_value("${accessKeyEnvVarName}")
                # RECOMMENDED: use environment variables for accessKey for security reasons
                try:
                        accessKey = os.environ[accessKeyEnvVarName]
                except KeyError:
                        accessKey = self.build_in.get_variable_value("${accessKey}")

                if not accessKey:
                        self.build_in.fail("Access key '{}' is empty, please set accessKey as a environment variable and provide its name in the accessKeyEnvVarName variable.".format(accessKeyEnvVarName))
                        return -1

                self.platform_name = platformName
                self.app_package = androidPackage
                self.app_activity = androidActivity
                appium_version = appiumVersion
                test_name = suite_name
                device_query = deviceQuery
                self.bundle_id = bundleId
                self.app = appCloudName
                # self.newCommandTimeout = newCommandTimeout

                if self.app:
                        self.build_in.log_to_console("app: {}".format(self.app))
                else:
                        self.build_in.log_to_console("app: is None or empty")

                self.build_in.log_to_console("cloudUrl: {}".format(cloudUrl))
                self.build_in.log_to_console("platformName: {}".format(self.platform_name))
                self.build_in.log_to_console("appPackage: {}".format(self.app_package))
                self.build_in.log_to_console("appActivity: {}".format(self.app_activity))
                self.build_in.log_to_console("appiumVersion: {}".format(appiumVersion))
                self.build_in.log_to_console("suiteName in reporter: {}".format(test_name))
                self.build_in.log_to_console("deviceQuery: {}".format(device_query))
                self.build_in.log_to_console("bundleId: {}".format(bundleId))
                for key, value in kwargs.items():
                        self.build_in.log_to_console("kwargs - {}: {}".format(key, value))
                self.build_in.log_to_console("log level: {}\n".format(self.build_in.get_variable_value("${LOG LEVEL}")))

                if self.platform_name in ["ios", "iOS", "IOS"]:
                        if not self.app:
                                app="cloud:{}".format(self.bundle_id)
                        else:
                                app = appCloudName
                        result = self.open_application( self.build_in.get_variable_value("${cloudUrl}"),
                                                        accessKey=accessKey,
                                                        app=app,
                                                        platformName="ios",
                                                        bundleId=self.bundle_id,
                                                        appiumVersion=appium_version,
                                                        testName=test_name,
                                                        deviceQuery=device_query,
                                                        **kwargs)
                elif self.platform_name in ["android", "Android", "ANDROID"]:
                        if not self.app:
                                app="cloud:{}/{}".format(self.app_package, self.app_activity)
                        else:
                                app=appCloudName
                        result = self.open_application( self.build_in.get_variable_value("${cloudUrl}"),
                                                        accessKey=accessKey,
                                                        app=app,
                                                        platformName="android",
                                                        appPackage=self.app_package,
                                                        appActivity=self.app_activity,
                                                        appiumVersion=appium_version,
                                                        testName=test_name,
                                                        deviceQuery=device_query,
                                                        **kwargs)
                else:
                        self.build_in.fail("platformName is not supported: {}".format(self.platform_name))
                        result = -1

                if log_level == 'DEBUG':
                        self.build_in.log_to_console("open application result: {}".format(result))
                
                self.driver = self._current_application

        def stop_session(self):
                self.close_application()

        def do_some_magic(self):
                self.report("Lord Voldemort loves Harry Potter", True)
        
        def do_some_black_magic(self):
                self.report("Lord Voldemort hates Harry Potter", False, True)

        def get_platform_specific_locator(self, locator_name):
                '''This method is used to get the platform specific locator from the dictionary'''
                if locator_name.startswith("xpath=") or locator_name.startswith("id="):
                        return locator_name;
                if self.platform_name in ["ios", "iOS", "IOS"]:
                        if ios_locators[locator_name]:
                                return ios_locators[locator_name]
                        else:
                                self.build_in.fail("Locator not found in the ios_locators dictionary: {}".format(locator_name))
                                return -1
                elif self.platform_name in ["android", "Android", "ANDROID"]:
                        if android_locators[locator_name]:
                                return android_locators[locator_name]
                        else:
                                self.build_in.fail("Locator not found in the android_locators dictionary: {}".format(locator_name))
                                return -1
                else:
                        self.build_in.fail("platform is not supported: {}".format(self.platform_name))
                        return -1

        # REPORTER ------------------------------------------------------------------------

        def report(self, message, status, teardown=False):
                # self.build_in.log_to_console("\nreporting message: {}, status: {}".format(message, status))
                if isinstance(status, bool) and isinstance(message, str):
                        if self.build_in.get_variable_value("${LOG LEVEL}") == 'DEBUG':
                                self.build_in.log_to_console("\nreporting message: {}, status: {}".format(message, status))
                        if not message:
                                message = "No info"
                        message = message.split("\n")[0] # takes only 1st line of the message
                        self.execute_script("seetest:client.report(\"{}\", {})".format(message, status))        # in case status=False report will not be failed
                        if not status and teardown:
                                # if you need to force exception in robot (has impact on the report structure, not recommended)
                                self.build_in.fail("{} failed".format(message))
                else:
                        self.build_in.log_to_console("Status has to be boolean, instead got: {}".format(type(status)))

        def start_steps_group(self, name):
                self.execute_script("seetest:client.startStepsGroup(\"{}\")".format(name))

        def stop_steps_group(self):
                self.execute_script("seetest:client.stopStepsGroup()")

        def start_group(self):
                '''Start group inside another keyword, allows to pass that top level keyword as a group name to DAI reporter'''
                self.execute_script("seetest:client.startStepsGroup(\"{}\")".format(self._get_top_keyword_name()))

        def set_device_location(self, latitude, longitude):
                '''Set device location for the test''' 
                self.execute_script("seetest:client.setLocation({},{})".format(latitude, longitude))
        
        def stop_group(self):
                self.stop_steps_group()

        def set_group_status(self, status):
                if status in ["Passed", "Failed"]:
                        self.execute_script("seetest:client.setGroupStatus(\"{}\")".format(status))
                else:
                        self.build_in.fail("status is not supported: {}".format(status))

        def set_report_status(self, status, failed_tests_names="at least one test failed"):
                if isinstance(status, bool):
                        if status:
                                self.execute_script("seetest:client.setReportStatus(\"Passed\", \"all tests passed\")")
                        else:
                                self.execute_script("seetest:client.setReportStatus(\"Failed\", \"{}\")".format(failed_tests_names))
                else:
                        self.build_in.fail("status has to be boolean")

        def steps_group_action_teardown(self, error=None):
                if error:
                        self.set_group_status("Failed")
                        safe_error = str(error).replace('"', '')
                        self.report("Error occurred in the test: {}".format(safe_error), False)
                self.stop_steps_group()
        
        # SUITES ------------------------------------------------------------------------

        def register_suite_name(self, suiteName):
                self.add_test_property("suite-name", suiteName)

        def add_test_property(self, key, value):
                if log_level == 'DEBUG':
                        self.build_in.log_to_console("trying to add test property with key: {}, and value: {}".format(key, value))
                value = value.split("\n")[0] # takes only 1st line of the value
                self.execute_script("seetest:client.addTestProperty(\"{}\", \"{}\")".format(key, value))
        
        def get_test_property(self, property_name):
                property = self.get_capability(property_name)
                self.build_in.log_to_console("\n{}: {}".format(property_name, property))
                return property

        def perform_suite_setup_actions(self, suiteName, with_unique_stamp=False, **kwargs):
                self.build_in.log_to_console("suiteName: {}".format(suiteName))
                self.build_in.log_to_console("with_unique_stamp: {}".format(with_unique_stamp))
                self.build_in.log_to_console("kwargs: {}".format(kwargs))
                if with_unique_stamp:
                        self.start_session("{} {}".format(suiteName, datetime.now().strftime('%Y%m%d_%H%M%S')), **kwargs)
                else:
                        self.start_session(suiteName, **kwargs)
                self.start_steps_group("Preparing Test Suite")
                self.register_suite_name(suiteName)
                self.add_test_property("unique_stamp", self.unique_stamp)
                
                self.stop_steps_group()

        def perform_suite_teardown_actions(self):
                self.start_steps_group("Test Suite Summary")
                suite_status = self.build_in.get_variable_value("${SUITE_STATUS}")
                self.build_in.log_to_console("Suite status is: {}".format(suite_status))

                for test_result in self.test_results:
                        if test_result['test_status']:
                                text_for_reporter = "Scenario: '{}' passed".format(test_result['test_case_name'])
                        elif not test_result['test_status']:
                                # text_for_reporter = "Scenario: '{}' failed".format(test_result['test_case_name'])
                                text_for_reporter = "Scenario: '{}' failed with result: {}".format(test_result['test_case_name'], test_result['test_failure_cause'])
                        else:
                                text_for_reporter = "Test logic error: please check test scripts to debug the issue"
                        try:
                                # self.build_in.log_to_console("Reporting test result: {}".format(text_for_reporter))
                                # self.build_in.log_to_console("Status: {} of type: {}".format(test_result['test_status'], type(test_result['test_status'])))
                                self.report(message=text_for_reporter, status=test_result['test_status'])
                        except Exception as e: 
                                self.build_in.log_to_console("Error in reporting test result: {}".format(e))

                text_separator = ' | '
                result_text = text_separator.join(self.failed_test_names).replace('"', '')
                if log_level == 'DEBUG':
                        self.build_in.log_to_console("\n>>>><<<<\n"+result_text+"\n>>>><<<<\n")

                if self.failed_test_names:
                        self.set_report_status(False, result_text)
                else:
                        self.set_report_status(True)


                self.stop_steps_group()
                self.stop_session()
        
        # TESTS ------------------------------------------------------------------------

        def register_test_name(self, name: str, status: str):
                if status in ['PASS', 'FAIL']:
                        if status == 'PASS':
                                self.add_test_property("test: "+name, "passed")
                        else:
                                self.add_test_property("test: "+name, "failed")
                

        def register_test_tags(self):
                test_tags = self.build_in.get_variable_value("${TEST_TAGS}")
                if test_tags:
                        self.build_in.log_to_console("Test tags are: {}".format(test_tags))
                        for test_tag in test_tags:
                                self.add_test_property("test-tag-{}".format(test_tag), "registered")


        def perform_test_setup_actions(self, with_app_activation=True):
                test_name = self.build_in.get_variable_value("${TEST_NAME}")

                self.start_steps_group("Test Case > {}".format(test_name))

                self.start_steps_group("perform test setup actions")
        
                self.register_test_tags()
                try:
                        if with_app_activation:
                                if self.platform_name in ["ios", "iOS", "IOS"]:
                                        self.activate_application(self.bundle_id)
                                elif self.platform_name in ["android", "Android", "ANDROID"]:
                                        self.activate_application(self.app_package)
                        else:
                                self.report("Application was not activated in test setup.", True)
                except Exception as e:
                        self.build_in.fail("Exception: {}".format(e))
                        self.build_in.log_to_console("Exception: {}".format(e))
                self.stop_steps_group()

        def perform_test_teardown_actions(self, with_app_activation=True):
                self.start_steps_group("perform test teardown actions")
                
                test_name = self.build_in.get_variable_value(name="${TEST_NAME}")
                test_status = self.build_in.get_variable_value(name="${TEST_STATUS}")

                # we are marking test red in teardown in case one of Appium methods failed (it does not fail in the Digital.ai reporter by default)
                self.build_in.run_keyword_if_test_passed("Set Group Status", "Passed")
                self.build_in.run_keyword_if_test_failed("Set Group Status", "Failed")

                if test_status == "FAIL":
                        test_msg = self.build_in.get_variable_value("${TEST_MESSAGE}")
                        safe_msg = test_msg.replace('"', '')
                        test_entry = {"test_case_name": test_name, "test_failure_cause": safe_msg, "test_status": False}
                        self.test_results.append(test_entry)
                        self.failed_test_names.append(test_msg)
                        if test_name and safe_msg:
                                # self.build_in.log_to_console("\nerror msg: {}".format(test_msg))
                                self.add_test_property("error in: {}".format(test_name), " msg: {}".format(safe_msg))
                                self.report("msg: {}".format(safe_msg), False)
                elif test_status == 'PASS':
                        test_entry = {"test_case_name": test_name, "test_failure_cause": "", "test_status": True}
                        self.test_results.append(test_entry)

                if with_app_activation:
                        if self.platform_name in ["ios", "iOS", "IOS"]:
                                self.terminate_application(self.bundle_id)
                        elif self.platform_name in ["android", "Android", "ANDROID"]:
                                self.terminate_application(self.app_package)
                else:
                        self.report("Application was not terminated in test teardown.", True)

                self.register_test_name(test_name, test_status)

                self.stop_steps_group()
                self.stop_steps_group()
                

        # APPIUM WRAPPERS ------------------------------------------------------------------------
        # for those that produce more than one entry in the reporter we need a wrapper
        
        @keyword
        @handle_exceptions
        def start_application(self):
                if self.platform_name in ["ios", "iOS", "IOS"]:
                        self.activate_application(self.bundle_id)
                elif self.platform_name in ["android", "Android", "ANDROID"]:
                        self.activate_application(self.app_package) 

        @keyword
        @handle_exceptions
        def stop_application(self):
                if self.platform_name in ["ios", "iOS", "IOS"]:
                        self.terminate_application(self.bundle_id)
                elif self.platform_name in ["android", "Android", "ANDROID"]:
                        self.terminate_application(self.app_package)

        @keyword
        @handle_exceptions
        def click_element(self, locator):
                locator = self.get_platform_specific_locator(locator)
                return super().click_element(locator)
        
        @keyword
        @handle_exceptions
        def click_with_offset(self, locator, x_offset, y_offset, duration=500):
                locator = self.get_platform_specific_locator(locator)
                element_location = self.get_element_location(locator)
                if log_level == 'DEBUG':
                        self.build_in.log_to_console("\nElement location: {}".format(element_location))
                element_x = element_location['x']
                element_y = element_location['y']
                if log_level == 'DEBUG':
                        self.build_in.log_to_console("\nOffset: x: {}, y: {}".format(x_offset, y_offset))
                tap_x = int(element_x) + int(x_offset)
                tap_y = int(element_y) + int(y_offset)
                if log_level == 'DEBUG':
                        self.build_in.log_to_console("\nTapping at x: {}, y: {}".format(tap_x, tap_y))
                return super().tap_with_positions(duration, (tap_x, tap_y))
        
        @keyword
        @handle_exceptions
        def click_with_offset_ratio(self, locator, percent_x, percent_y, duration=500):
                """
                Clicks on the element with the offset calculated as a percentage of the element's width and height\n
                @param locator: locator of the element (xpath, id, etc.)\n
                @param percent_x: percentage of the element's width in range 0-1 eg. 0.94 for 94%\n
                @param percent_y: percentage of the element's height in range 0-1 eg. 0.5 for 50%\n
                @param duration: duration of the tap in milliseconds\n
                """
                locator = self.get_platform_specific_locator(locator)
                # element_location = self.get_element_location(locator)
                element_rect = self.get_element_rect(locator)
                if log_level == 'DEBUG':
                        self.build_in.log_to_console("\nElement location: {}".format(element_rect))
                element_x = element_rect['x']
                element_y = element_rect['y']
                element_width = element_rect['width']
                element_height = element_rect['height']
                offset_x = int(int(element_width) * float(percent_x))
                offset_y = int(int(element_height) * float(percent_y))
                if log_level == 'DEBUG':
                        self.build_in.log_to_console("\nOffset: x: {}, y: {}".format(offset_x, offset_y))
                tap_x = int(element_x) + int(offset_x)
                tap_y = int(element_y) + int(offset_y)

                if log_level == 'DEBUG':
                        self.build_in.log_to_console("\nTapping at x: {}, y: {}".format(tap_x, tap_y))
                return super().tap_with_positions(duration, (tap_x, tap_y))
        
        @keyword
        @handle_exceptions
        def wait_and_click_element(self, locator, timeout=global_timeout):
                locator = self.get_platform_specific_locator(locator)
                super().wait_until_page_contains_element(locator, timeout)
                return super().click_element(locator)
        
        @keyword
        @handle_exceptions
        def input_text(self, locator, text):
                locator = self.get_platform_specific_locator(locator)
                if log_level == 'DEBUG':
                        self.build_in.log_to_console("\nDEBUG | locator: {}, text: {}".format(locator, text))
                return super().input_text(locator, text)

        @keyword
        @handle_exceptions
        def page_should_contain_element(self, locator, loglevel='INFO'):
                locator = self.get_platform_specific_locator(locator)
                return super().page_should_contain_element(locator, loglevel=loglevel)
        
        @keyword
        @handle_exceptions
        def page_should_not_contain_element(self, locator, loglevel='INFO'):
                locator = self.get_platform_specific_locator(locator)
                return super().page_should_not_contain_element(locator, loglevel=loglevel)
        
        @keyword
        @handle_exceptions
        def page_should_contain_text(self, locator, loglevel='INFO'):
                locator = self.get_platform_specific_locator(locator)
                return super().page_should_contain_text(locator, loglevel=loglevel)
        
        @keyword
        @handle_exceptions
        def page_should_not_contain_text(self, locator, loglevel='INFO'):
                locator = self.get_platform_specific_locator(locator)
                return super().page_should_not_contain_text(locator, loglevel=loglevel)

        @keyword
        @handle_exceptions
        def swipe(self, x_start, x_stop, y_start, y_stop, duration=1000):
                return super().swipe(start_x=x_start, start_y=y_start, offset_x=x_stop, offset_y=y_stop, duration=duration)
        
        @keyword
        @handle_exceptions
        def swipe_to_element(self, x_start, y_start, element_xpath, duration=1000, direction='up', max_swipes=10, swipe_distance=200):
                if direction == 'up':
                        offsetX = 0
                        offsetY = -swipe_distance
                elif direction == 'down':
                        offsetX = 0
                        offsetY = swipe_distance
                elif direction == 'left':
                        offsetX = -swipe_distance
                        offsetY = 0
                elif direction == 'right':
                        offsetX = swipe_distance
                        offsetY = 0

                for i in range(max_swipes):
                        try:
                                super().page_should_contain_element(element_xpath)
                                return True
                        except Exception as e:
                                if log_level == 'DEBUG':
                                        self.build_in.log_to_console("\nElement not found, swiping...")
                                self.swipe(x_start, x_start+offsetX, y_start, y_start+offsetY, duration)

                try:
                        super().page_should_contain_element(element_xpath)
                        return True
                except Exception as e:
                        self.build_in.log_to_console("\nElement not found after swiping; xpath: "+element_xpath)
                        raise e

        @keyword
        @handle_exceptions
        def wait_activity(self, activity, timeout=global_long_timeout, interval=1):
                return super().wait_activity(activity, timeout, interval)

        @keyword
        @handle_exceptions
        def wait_until_element_is_visible(self, locator, timeout=None, error=None):
                locator = self.get_platform_specific_locator(locator)
                return super().wait_until_element_is_visible(locator, timeout, error)

        @keyword
        @handle_exceptions
        def wait_until_page_contains(self, text, timeout=None, error=None):
                return super().wait_until_page_contains(text, timeout, error) 

        @keyword
        @handle_exceptions
        def wait_until_page_contains_element(self, locator, timeout=None, error=None):
                locator = self.get_platform_specific_locator(locator)
                return super().wait_until_page_contains_element(locator, timeout, error)
        
        @keyword
        @handle_exceptions
        def wait_until_page_does_not_contain(self, text, timeout=None, error=None):
                return super().wait_until_page_does_not_contain(text, timeout, error)
        
        @keyword
        @handle_exceptions
        def wait_until_page_does_not_contain_element(self, locator, timeout=None, error=None):
                locator = self.get_platform_specific_locator(locator)
                return super().wait_until_page_does_not_contain_element(locator, timeout, error)

        @keyword
        @handle_exceptions
        def input_password(self, locator, text):
                locator = self.get_platform_specific_locator(locator)
                return super().input_password(locator, text)
        
        @keyword
        @handle_exceptions
        def clear_text(self, locator):
                locator = self.get_platform_specific_locator(locator)
                return super().clear_text(locator)

        @keyword
        @handle_exceptions
        def scroll(self, start_locator, end_locator):
                start_locator = self.get_platform_specific_locator(start_locator)
                end_locator = self.get_platform_specific_locator(end_locator)
                return super().scroll(start_locator, end_locator)
        
        @keyword
        @handle_exceptions
        def scroll_element_into_view(self, locator):
                locator = self.get_platform_specific_locator(locator)
                return super().scroll_element_into_view(locator)
        
        @keyword
        @handle_exceptions
        def scroll_down(self, locator):
                locator = self.get_platform_specific_locator(locator)
                return super().scroll_down(locator)
        
        @keyword
        @handle_exceptions
        def scroll_up(self, locator):
                locator = self.get_platform_specific_locator(locator)
                return super().scroll_up(locator)
        
        @keyword
        @handle_exceptions
        def implicit_wait(self, time, reason=""):
                return self.build_in.sleep(time_=time, reason=reason)
        
        @keyword
        @handle_exceptions
        def element_should_be_visible(self, locator, loglevel='INFO'):
                return super().element_should_be_visible(locator, loglevel)
        
        @keyword
        @handle_exceptions
        def page_should_contain_text(self, text, loglevel='INFO'):
                return super().page_should_contain_text(text, loglevel)

        # DAI FEATURES ------------------------------------------------------------------------

        @keyword
        @handle_exceptions
        def start_performance_transaction(self, nv_profile='Monitor'):
                '''
                Network profiles can be found in cloud settings under "Network Profiles" menu.
                Examples:
                        3G-bad-connection
                        3G-High-Latency
                        3G-Lossy
                        3G-average
                        4G-bad-connection
                        4G-High-Latency
                        4G-Lossy
                        4G-average
                        Monitor

                '''
                return self.execute_script("seetest:client.startPerformanceTransaction(\"{}\")".format(nv_profile) )
        
        @keyword
        @handle_exceptions
        def end_performance_transaction(self, name):
                return self.execute_script("seetest:client.endPerformanceTransaction(\"{}\")".format(name))

        @keyword
        @handle_exceptions
        def start_performance_transaction_for_application(self, app_package, nv_profile="Monitor"):
                return self.execute_script(f"seetest:client.startPerformanceTransactionForApplication(\"{app_package}\", \"{nv_profile}\")")
        
        @keyword
        @handle_exceptions
        def activate_voice_assistance(self, command="open google"):
                return self.execute_script(f"seetest:client.activateVoiceAssistance(\"{command}\")")

        # IOS SPECIFIC FEATURES ------------------------------------------------------------------------

        # ANDROID SPECIFIC FEATURES ------------------------------------------------------------------------
