<h1 align="center"><b>Twilight Princess Ultimate Edition (GCN USA)</b></h1>
<p align="center">
  <img src="https://github.com/TP-Ultimate-Edition/.github/raw/main/banner.png" width="720" alt="Twilight Princess Ultimate Edition Banner">
</p>

<hr>

<h2><b>🚫 IMPORTANT LEGAL NOTICE — READ BEFORE CONTINUING</b></h2>
<p>
  <b>We do NOT distribute game assets or ISO files.</b><br>
  <b>We will NEVER provide, upload, or link to copyrighted ROMs, ISOs, or extracted game data.</b><br>
  You must supply your own <b>LEGITIMATE personal dump</b> of the GameCube USA version (GZ2E01).
</p>
<p>This project only provides:</p>
<ul>
  <li>Decompiled code</li>
  <li>Tools</li>
  <li>Scripts</li>
  <li>Engine patches</li>
  <li>Instructions</li>
</ul>
<p><b>You are responsible for obtaining your own legal copy of the game and dumping it yourself.</b></p>

<hr>

<h2><b>⚠️ Version Compatibility Notice</b></h2>
<p>
  <b>This project only works with the GameCube USA version (GZ2E01).</b><br>
  No PAL, Japanese, or Wii versions are supported.<br>
  Using any ISO other than <b>GZ2E01</b> will result in errors or a broken build.
</p>

<hr>

<h2><b>⭐ Features</b></h2>
<ul>
  <li>True 60FPS engine via delta-time physics</li>
  <li>Correct animation & gameplay timing at 60FPS</li>
  <li>Resolution scaling for modern hardware</li>
  <li>QoL improvements inspired by Twilight Princess HD</li>
  <li>Windows + Linux ISO building included</li>
  <li>Dolphin-optimized output</li>
</ul>

<hr>

<h2><b>🚨 IMPORTANT BUILD PREREQUISITE</b></h2>
<p>
  Before using any ISO build script:<br>
  <b>You must successfully complete a normal decomp build using the USA (GZ2E01) ISO.</b><br>
  If the standard build fails, the ISO build will also fail.
</p>

<hr>

<h2><b>🔧 Dependencies</b></h2>

<h3>🪟 Windows</h3>
<ol>
  <li>
    <b>Install Python 3.14.0 (64-bit)</b><br>
    Download: <a href="https://www.python.org/ftp/python/3.14.0/python-3.14.0-amd64.exe">Python 3.14.0</a><br>
    Verify:
    <pre>python --version
pip --version</pre>
  </li>
  <li>
    <b>Install Ninja</b><br>
    <pre>winget install Ninja-build.Ninja</pre>
    or
    <pre>pip install ninja</pre>
  </li>
  <li>
    <b>Install gclib</b><br>
    <pre>pip install "gclib[speedups] @ git+https://github.com/LagoLunatic/gclib.git"</pre>
  </li>
</ol>

<h3>🐧 Linux</h3>
<p>Install Python + Ninja:</p>
<pre>sudo apt install python3 python3-pip ninja-build</pre>
<p>(or your distro equivalent)</p>
<p>Install gclib:</p>
<pre>pip3 install "gclib[speedups] @ git+https://github.com/LagoLunatic/gclib.git"</pre>

<hr>

<h2><b>🏗️ Standard Decomp Build (Required First)</b></h2>
<p>Clone the repo:</p>
<pre>git clone https://github.com/TP-Ultimate-Edition/Twilight-Princess-Ultimate-Edition.git
cd Twilight-Princess-Ultimate-Edition</pre>

<p>Place your own legally dumped USA ISO at:</p>
<pre>orig/GZ2E01/baserom.iso</pre>

<p>Configure the project:</p>
<pre>python3 configure.py --version=GZ2E01</pre>

<p>Build:</p>
<pre>ninja</pre>

<p>A successful build produces:</p>
<ul>
  <li>Compiled REL modules</li>
  <li>build/GZ2E01/framework.iso</li>
</ul>

<hr>

<h2><b>💿 Windows ISO Build</b></h2>
<p>Run:</p>
<pre>build_iso.bat</pre>

<p>You will be prompted for:</p>
<ul>
  <li><b>Your Dolphin Emulator path only</b></li>
</ul>

<p>The script will:</p>
<ul>
  <li>Use your existing <code>orig/GZ2E01/baserom.iso</code></li>
  <li>Rebuild all RELs</li>
  <li>Produce the patched 60FPS Ultimate Edition ISO</li>
  <li>Output a Dolphin-ready image</li>
</ul>

<h2><b>🐍 Linux ISO Build</b></h2>
<p>Run the included script:</p>
<pre>python3 build_iso_linux.py</pre>

<p>It will:</p>
<ul>
  <li>Ask for your output ISO name</li>
  <li>Compile a patched 60FPS ISO</li>
  <li>Output a Dolphin-ready image</li>
</ul>

<hr>

<h2><b>⚡ 60FPS Engine Overview</b></h2>
<ul>
  <li>Frame-rate–independent delta-time physics</li>
  <li>Proper 60FPS animations & movement</li>
  <li>Smooth, stable gameplay</li>
  <li>Resolution scaling</li>
  <li>Optional TPHD-style QoL enhancements</li>
</ul>

<hr>

<h2><b>📘 Modding & Contributions</b></h2>
<p>Before modifying RELs or engine code:</p>
<p>→ Please read <b>Modding Guide.pdf</b>.</p>
<p>It covers:</p>
<ul>
  <li>Correct REL editing workflow</li>
  <li>Build system requirements</li>
  <li>How to avoid incompatible or broken builds</li>
  <li>Maintaining 60FPS engine stability</li>
</ul>

<hr>

<h2><b>🙏 Credits</b></h2>

<h3>🏹 Zelda Reverse Engineering Team</h3>
<p>For fully decompiling the GameCube USA (GZ2E01) version of Twilight Princess.<br>
This project exists thanks to their foundational work.</p>

<h3>🔧 Carco</h3>
<p>For essential research and documentation regarding:</p>
<ul>
  <li>REL internals</li>
  <li>REL patching methodology</li>
  <li>ISO rebuild processes</li>
</ul>
<p>Their work made advanced engine modifications possible.</p>

<p align="center"><b>Enjoy Twilight Princess in smooth, modern 60FPS — using your own legitimate USA GCN dump!</b></p>
