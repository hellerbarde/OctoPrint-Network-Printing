## IMPORTANT!

if your network is not stable, this plugin might not be for you. I have had good experiences with it so far, 
but if there are interruptions in network traffic, your print might stop or be jittery, resulting in printing irregularities.
I take no responsibility for any failed prints or worse.


# OctoPrint-Network-Printing

OctoPrint-Network-Printing enables OctoPrint to use the Python-internal serial-over-network functionality to connect to
a 3d printer over the network, or even WiFi.

It supports both RFC2217, and raw TCP socket protocols. The raw TCP socket protocol works with the ESP3D project,
if that is of interest. At the time of writing, I am not aware of any ESP32 or ESP8266 projects that implement 
RFC2217 correctly. Please open an issue to let me know if you become aware of one. 


## Setup

Install via the bundled [Plugin Manager](https://docs.octoprint.org/en/master/bundledplugins/pluginmanager.html)
or manually using this URL:

    https://github.com/hellerbarde/OctoPrint-Network-Printing/archive/main.zip

After installation, follow the Configuration section below to set up the address of your printer.


## Configuration

Configuration is currently done through the "Additional Serial Ports" global config. This should probably change in the future, but it works well for now.

If you have an RFC2217 adapter, use this syntax: `rfc2217://<hostname or ip>:<port>`, for example `rfc2217://my3dprinter.local:8888` or `rfc2217://10.0.1.125:8888`

If you have an Serial-to-IP adapter that uses a "raw", i.e. non-RFC2217 protocol, use this syntax: `socket://<hostname or ip>:<port>`, for example `socket://my3dprinter.local:8888` or `socket://10.0.1.125:8888`.
As far as I can tell, ESP3D uses the `socket` protocol.