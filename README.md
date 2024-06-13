<h1>Example project boilerplate code for Robot Framework and Digital.ai's reporter integration.</h1>

<h2>Content</h2>
This repository contains basic setup for Robot Framework and Digital.ai Continuous Testing solution. 
<a href="https://digital.ai/products/continuous-testing/">https://digital.ai/products/continuous-testing/</a>

<br>
The project core is written with Python (daiMobileLibrary.py) which can be easily added to existing project to reuse, or it can be used as a starting point. Once imported you can start using Digital.ai Robot Framework keywords in your project. 

<h2>Example </h2>
<h3>Test report before the changes (pure Robot Framework)</h3>

![Example Image](images/before.png)

<h3>Test report after the changes (with Digital.ai library)</h3>

![Example Image](images/after.png)

<h3>Reports page in digital.ai Continuous Testing cloud</h3>

![Example Image](images/reports.png)

<h2>Project file structure:</h2>
<ul>
    <li><b>resources/capabilities/</b> - holds example capabilities for devices: Android and iOS device, and Chrome browser</li>
    <li><b>resources/cloudCredentials.robot</b> - holds cloud credentials (cloud URL and access key)</li>
    <li><b>resources/daiMobileLibrary.py</b> - contains definitions, logic and keywords for DAI reporter</li>
    <li><b>steps/</b> - contains an extra layer of business logic (BDD)</li>
    <li><b>tests/</b> - contains tests files</li>
    <li><b>results/</b> - destination folder for test results</li>
</ul>

<h2>Setup</h2>
<h3>To install dependenecies:</h3>
<code>pip install -r requirements.txt</code>
<h3>Cloud and device settings</h3>
After getting access key and setting cloud related paramters in cloudCredentials.robot please set platform name and deviceQuery in deviceCapabilities.


<h2>Execution</h2>
To run test script in the command line:<br/>
<code>robo -d results/ tests/androidNativeApp.robot </code><br/>
<code>robo -d results/ tests/*</code>


<h2>Tests</h2>
There are few ready to use test cases <br>
<ul>
    <li><b>tests/examples/daiFeatures.robot</b> - contains examples of Digital.ai features like measuring performance and voice assistance</li>
    <li><b>tests/examples/daiReporter.robot</b> - contains examples of tests to showcase reporter capabilities</li>
</ul>
<br/>
<br/>
<br/>
<i>This project is work in progress, please report any issues or suggest changes</i>
