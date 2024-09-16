'''
Top level capabilities. Here you can select platform and/or define deviceQuery.
Specific platform capabilities are define in groups below.
All capabilities here are required.
'''
appiumVersion='2.5.2'
platformName='android'
deviceQuery=f"@os='{platformName}' and not(tag='dirty')"    # deviceQuery is used to select a device

appCloudName='cloud:uniqueName=AppiumOssAndroid'    # it is translate to 'app' capability

# Android specific
androidPackage='com.experitest.ExperiBank'
androidActivity='.LoginActivity'

# iOS specific
bundleId='com.experitest.ExperiBank'
