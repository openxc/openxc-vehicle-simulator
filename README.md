openxc-vehicle-simulator
======================

## Running the Emulator

First install Flask:
      flask.pocoo.org/docs/installation

Next, run the script emulate.py.

To open the UI, open a browser and navigate to http://localhost:5000/

To connect with an Android device, open the Enabler activity, open the settings, choose Data Sources, and enable "Use a network device".

Set the host address to the address of the machine running emulate.py, and set the port to 50001.  (You may nhttp://localhost:5000/eed to disable and re-enable "Use a network device" after entering the correct information.)  The terminal running emulate.py should indicate that it received a new connection.