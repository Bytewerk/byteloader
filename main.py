#!/usr/bin/python3
# -*- coding: utf-8 -*-



import sys
from byteLoader import ByteLoader
from can import CanBus



def main( ):
	if len( sys.argv ) != 3:
		print( 'Provide CAN device name as interface(e.g. can0)' )
		print( sys.argv[0], '<interface> <hexfile>' )
		sys.exit( 0 )

	interface = sys.argv[1]
	hexfile = sys.argv[2]

	canBus = CanBus( interface )

	bl = ByteLoader( canBus )
	bl.importHexFile( hexfile )
	rc = bl.run( )

	if rc:
		exit( rc ) # die with errorcode
# end main

main( )