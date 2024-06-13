<h1>This is example project boilerplate code for Robot Framework and Digital.ai's reporter integration.</h1>

<h3>Project file structure:</h3>
<ul>
    <li><b>resources/capabilities/</b> - holds example capabilities for devices: Android and iOS device, and Chrome browser</li>
    <li><b>resources/cloudCredentials.robot</b> - holds cloud credentials (cloud URL and access key)</li>
    <li><b>resources/daiMobileLibrary.py</b> - contains definitions, logic and keywords for DAI reporter</li>
    <li><b>steps/</b> - contains an extra layer of business logic (BDD)</li>
    <li><b>tests/</b> - contains tests files</li>
    <li><b>results/</b> - destination folder for test results</li>
</ul>

<h3>Setup</h3>
<h4>To install dependenecies:</h4>
<code>pip install -r requirements.txt</code>
<h4>Cloud and device settings</h4>
After getting access key and setting cloud related paramters in cloudCredentials.robot please set platform name and deviceQuery in deviceCapabilities.


<h3>Execution</h3>
To run test script in the command line:<br/>
<code>robo -d results/ tests/androidNativeApp.robot </code><br/>
<code>robo -d results/ tests/*</code>


<h3>Tests</h3>
There are few ready to use test cases <br>
<ul>
    <li><b>tests/examples/daiFeatures.robot</b> - contains examples of Digital.ai features like measuring performance and voice assistance</li>
    <li><b>tests/examples/daiReporter.robot</b> - contains examples of tests to showcase reporter capabilities</li>
</ul>
<br/>
<br/>
<br/>
<i>This project is work in progress, please report any issues or suggest changes</i>