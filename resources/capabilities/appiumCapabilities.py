'''
Top level capabilities. Here you can select platform and/or define deviceQuery.
Specific platform capabilities are define in groups below.
All capabilities here are required.
'''
appiumVersion='2.2.2'
platformName='android'
deviceQuery=f"@os='{platformName}' and @category='PHONE'"

# Android specific
androidPackage='com.experitest.ExperiBank'
androidActivity='.LoginActivity'

# iOS specific
bundleId='com.experitest.ExperiBank'
