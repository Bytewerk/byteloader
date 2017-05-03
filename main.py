#!/usr/bin/python3
# -*- coding: utf-8 -*-

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

import sys
from byteLoader import ByteLoader
from can import CanBus



def main( ):
	if len( sys.argv ) != 3:
		print( 'Provide CAN device name as interface(e.g. can0)' )
		print( sys.argv[0], '<interface> <binfile>' )
		sys.exit( 0 )
		
	print( '' )
	print( 'ByteLoader  Copyright (C) 2015 - 2017  Daniel Steuer' )
	print( 'This program comes with ABSOLUTELY NO WARRANTY.' )
	print( 'This is free software, and you are welcome to redistribute it under certain conditions.' )

	interface = sys.argv[1]
	hexfile = sys.argv[2]

	canBus = CanBus( interface )

	bl = ByteLoader( canBus )
	bl.importBinFile( hexfile )
	rc = bl.run( )

	if rc:
		exit( rc ) # die with errorcode
# end main

main( )
