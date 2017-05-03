#!/bin/bash

# ByteLoader - a python program that talks to the kreatives-chaos CAN bootloader
#
# Copyright (C) 2015 - 2017  Daniel Steuer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

BITRATE=$1

if [ -z "$BITRATE" ]; then
	BITRATE=500000
fi

sudo ip link set can0 down
sudo ip link set can0 up type can bitrate $BITRATE

echo "I executed: ip link set can0 up type can bitrate $BITRATE"

candump -c can0,0:0,#FFFFFFFF
