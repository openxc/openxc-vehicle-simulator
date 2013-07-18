openxc-vehicle-simulator
======================

The OpenXC Vehicle Simulator is a web application built with
[Flask](flask.pocoo.org/docs/installation).

## Running the Emulator

First install the Python dependencies with `pip`:

      $ pip install pip-requirements.txt

To run the app:

      $ ./emulate.py

To open the UI, open a browser and navigate to http://localhost:5000/

To connect with an Android device, open the Enabler activity, open the settings,
choose Data Sources, and enable "Use a network device".

Set the host address to the address of the machine running emulate.py, and set
the port to 50001. You may need to disable and re-enable "Use a network device"
after entering the correct information. The terminal running emulate.py should
indicate that it received a new connection.
