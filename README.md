PLEXE Python Demos
==================

This repository includes some demo applications showing Plexe features
within SUMO using the TraCI interface via Python. The demo includes:

* A join maneuver demo, where a vehicle approaches a platoon of 8 cars
  and joins it in a certain position.
* An engine demo, which shows the features of the realistic engine
  model by running a sort of drag race between three different vehicle
  models: an Alfa Romeo 147, an Audi R8, and a Bugatti Veyron.

The code of the first example is implemented inside the `joindemo.py`
file, while the second inside `enginedemo.py`. You can simply run them
using

```
python joindemo.py
```
and
```
python enginedemo.py
```

After running for a certain amount of time, both demo resets and
automatically start from scratch (demo mode).

Alternatively, you can run them together with a dashboard, which shows
the RPM, the speed, the gear, and the acceleration of the vehicle being
tracked in the GUI. By tracking a different vehicle, the dashboard shows
the data of the chosen one.

To run the demos together with the dashboard type

```
python dashboard-demo.py joindemo.py
```
and
```
python dashboard-demo.py enginedemo.py
```

Running the dashboard requires you to install `PyQT5`. These demos
currently work with the latest experimental version of Plexe SUMO, which
can be downloaded [here](https://github.com/michele-segata/sumo-planetsumo.git).
Checkout and compile the `plexe-planetsumo-0.31.0` branch.

For more information on Plexe, visit
[http://plexe.car2x.org](http://plexe.car2x.org).
