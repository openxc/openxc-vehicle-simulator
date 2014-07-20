# Design doc for the OpenXC Vehicle simulator

### Purpose

The OpenXC Vehicle Simulator simulators the data stream from an OpenXC Vehicle
Interface.  It will run on a computer, and will simulate all of the signals
listed on the OpenXCPlatform.com Output Format page, at the listed frequencies.
The simulator will also take user input for the vehicle controls.  (Pedals,
steering wheel, etc.)  The generated JSON data will be displayed for the user
and sent to the Android host device via TCP connection.  The vehicle dynamics
model will be simple.  It will be modular, allowing for different vehicles, but
for the first version, accuracy will not be a priority.

The user interface will not be a driving simulator, merely a list of controls.
Controls will include sliders for pedals and the steering wheel, various radio
buttons and switches for other controls, etc.  Vehicle controls will include
everything needed to generate the above list of vehicle data, including doors
and lights.  While the fastest OpenXC signal is 60Hz, the vehicle dynamics model
will iterate fast enough to produce plausible data for things like the torque
and engine speed.  The world outside the car will be assumed to be a flat,
featureless sphere, solely for the purpose of generating GPS data.

### Components

Data Connection - The data connection with the OpenXC host device will be either
network or Bluetooth.  WiFi is more ubiquitous among target hardware, but
Bluetooth more closely simulates a connection to a Vehicle Interface.

Graphical User Interface - The GUI will allow real time user input.  (pedals,
gear, steering wheel, etc.)  The user will also have the option to set initial
vehicle values (odometer, fuel level, etc) as well as the update speed of the
different data types.  The GUI will also display the outgoing data to the user.
This is not intended to be any sort of video game, nor a simulation of the
driving experience.  It is only intended to simulate the data that might be
generated on the CAN bus.

State Manager - The Stage Manager will keep track of the simulation’s current
state, and handle sending that information to the TCP connection, the GUI, and
the Vehicle Dynamics Model.  The State Manager will also regulate how often each
piece of data is to be recalculated by the Vehicle Dynamics Model.  There will
be an initial default state that can be modified by the user before running.
The State Manager will not regulate data internal to the vehicle dynamics model.
(Air drag, road friction, etc.)  Nor will it be updated as fast as the vehicle
dynamics model.

Vehicle Dynamics Model - The Vehicle Dynamics Model will iterate at a
pre-determined rate.  (Tentatively 50 to 100Hz.)  Data will be kept in the
Vehicle Dynamics Model with a higher precision than is used in the CAN traffic.
(This will help reproduce conditions that have created failures in vehicles, but
did not fail with the current simulator.)  Data will only be sent to the State
Manager at the frequencies defined in the OpenXC data format.

A Note On Modularity - The components of the simulator will be as modular as
possible.  The State Manager and the Vehicle Dynamics Model will potentially be
useful in other applications.  A primary goal will be to have the GUI, State
Manager, and Vehicle Dynamics Model not be explicitly dependent on the
implementation of the other two.

### Open Questions

Should the simulator support the playback of trace files?  Or is this redundant?

Will the GUI be browser based, PyQt, or other?

Will the connection be network or Bluetooth?  What components of each already
exist in the current code base?

### Future Features

The application will be written in such a way as to facilitate future upgrades.
These are features that would be nice, but are not necessary in the first
version.  Once the above items are complete, these upgrades will be revisited.
If the ease of implementation and the usefulness of the feature warrant
inclusion, they will be added on then.

* Graphical dashboard - The User Interface will include a graphical
  representation of the dashboard, including speedometer, tachometer, and
  odometer, among other things.
* Hills - For the first version, the world will be a flat featureless sphere.
  For future versions, hilly terrain may prove useful for testing some projects.
* Specific vehicles - The goal of the first version is to create data that is
  plausible, not to model specific models and years of vehicle.  For future
  versions, it will be determined whether or not the accuracy of the physics
  model can be improved to the point where specific cars can be modeled.
