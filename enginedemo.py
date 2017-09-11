#!/usr/bin/env python
#
# Copyright (C) 2017 Michele Segata <msegata@disi.unitn.it>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

import os
import sys
import ccparams as cc
import random
from utils import add_vehicle, set_par, change_lane, get_par, start_sumo, \
    running

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")
import traci

# sumo launch command
sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "cfg/freeway.sumo.cfg"]


# vehicles to be inserted
VEHICLES = ["alfa-147", "audi-r8", "bugatti-veyron"]
TRACK = 1


def add_vehicles():
    """
    Adds the vehicles to the simulation
    """
    for i in range(len(VEHICLES)):
        vid = VEHICLES[i]
        add_vehicle(vid, 10, i, 0, 5)
        change_lane(vid, i)
        set_par(vid, cc.PAR_ACTIVE_CONTROLLER, cc.ACC)
        set_par(vid, cc.CC_PAR_VEHICLE_ENGINE_MODEL,
                cc.CC_ENGINE_MODEL_REALISTIC)
        set_par(vid, cc.CC_PAR_VEHICLES_FILE, "vehicles.xml")
        set_par(vid, cc.CC_PAR_VEHICLE_MODEL, vid)
        set_par(vid, cc.PAR_FIXED_ACCELERATION, cc.pack(1, 0))


def main(demo_mode, real_engine=True, setter=None):
    random.seed(1)
    start_sumo("cfg/freeway.sumo.cfg", False)
    step = 0

    while running(demo_mode, step, 4000):

        # when reaching 60 seconds, reset the simulation when in demo_mode
        if demo_mode and step == 4000:
            start_sumo("cfg/freeway.sumo.cfg", True)
            step = 0
            random.seed(1)

        traci.simulationStep()
        if step == 0:
            # create vehicles and track one of them
            add_vehicles()
            traci.gui.trackVehicle("View #0", VEHICLES[TRACK])
            traci.gui.setZoom("View #0", 20000)
        if step == 100:
            # at 1 second let them accelerate as much as they can
            for vid in VEHICLES:
                set_par(vid, cc.PAR_FIXED_ACCELERATION, cc.pack(1, 20))

        # in the dashboard, show the engine information about the vehicle
        # being tracked
        tracked_id = traci.gui.getTrackedVehicle("View #0")
        if setter is not None and tracked_id != "":
            (g, rpm) = cc.unpack(get_par(tracked_id, cc.PAR_ENGINE_DATA))
            data = get_par(tracked_id, cc.PAR_SPEED_AND_ACCELERATION)
            (v, a, u, x, y, t) = cc.unpack(data)
            setter(rpm, g, v, a)

        step += 1

    traci.close()


if __name__ == "__main__":
    main(True, True)
