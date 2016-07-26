# Round Owl's Fleet Monitor System

A telemetry monitoring and processing tool for truck simulators by SCS Software, inspired by truck manufacturers' Fleet Management Services.

Fleet Monitor System helps you identify and act upon the key details needed to increase the productivity of your fleet. Monitor technical data remotely by vehicle and by driver: fuel consumption, consumption in the green zone, percentage of time spent idling, number of times the brake pedal is pressed, etc. I've taken extra care to make sure the information you get is accurate and reliable.

## Installation
- Download and install Funbit's [Telemetry Web Server](https://github.com/Funbit/ets2-telemetry-server). ROFMS works through interacting with Telemetry Web Server's REST API.
- Download binary release archive and extract it.

## Usage
- Launch Telemetry Web Server, and either Euro Truck Simulator 2 or American Truck Simulator. For better experience go to Drive mode and assure that Telemetry Web Server gets the information from the truck.
- Launch telemetry_app.exe from the folder with extracted files.
- If you previously used the application, press Open and choose previously saved file.
- Set IP address to the address of Telemetry Web Server, then press "Connect".
- When done driving, press "Save" and choose file name in form of "Your ID.json", save it in the same folder.

## Using the web application
- Open "index.html" in your favorite web browser with JavaScript support.
- It will read all files saved in this folder and display them for you.
- If you've got data files (as described below) from another source, launch ROFMS (the game and TWS are not necessary), open the file you've got and save it in the folder with the app.

## Transferring data
- Send "Your ID.json" through any means of data transfer.
- "Your ID.0.json" contains very first data package you saved and will be used for trends monitoring.
