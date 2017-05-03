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


import socket
import struct
from sys import exit



if __name__ == "__main__":
	print( 'please run \'main.py\' instead' )
	exit( 0 )



class CanBus():
	def __init__( self, interface ):
		self.interface = interface #  ex.: "can0"
		# CAN frame packing/unpacking (see `struct can_frame` in <linux/can.h>)
		self.__can_frame_fmt = "=IB3x8s"

		# create a raw socket and bind it to the given CAN interface
		try:
			self.socket = socket.socket( socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW )
			self.socket.bind( (interface,) )
		except OSError:
			print( 'ERROR: OS Error' )
			exit( 10 )
	# __init__()



	def sendMsg( self, msg ):
		self.socket.settimeout( 2 )
		try:
			self.socket.send( self.__buildFrame( msg.id, msg.extended, msg.data) )
		except socket.error:
			print( 'ERROR: Cannot Send CAN frame' )
			return False
		return True
	# canSendData()



	def __buildFrame( self, can_id, ext, data ):
		can_dlc = len( data )

		data = data.ljust( 8, b'\x00' )
		id = can_id + (ext << 31)
		return struct.pack( self.__can_frame_fmt, id, can_dlc, data )
	#build_can_frame()



	def getMsgNonBlocking( self ):
		self.socket.settimeout( 0.25 )
		try:
			data, uselessMetaInfo = self.socket.recvfrom( 1024 )
		except socket.timeout:
			print( 'ERROR: Socket timeout' )
			return None

		except IOError:
			print( 'ERROR: IO Error' )
			return False

		disected = self.__dissectFrame(data)
		msg = CanMsg( self, disected[0], disected[1])
		msg.setData( disected[2] )
		return msg
	# getMsgNonBlocking()



	def __dissectFrame( self, frame ):
		can_id, can_dlc, data = struct.unpack( self.__can_frame_fmt, frame )

		# remove flags encoded into the id
		if can_id & 0x80000000:
			extended = True
			id = can_id & 0x1FFFFFFF
		else:
			extended = False
			id = can_id & 0x000007FF

		return (id, extended, data[:can_dlc])
	# dissect_can_frame()

# end class CanBus






class CanMsg( ):
	def __init__( self, canBus, id=0x7ff, extended=False ):
		self.id = id
		self.extended = extended
		self.data = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
		self.canBus = canBus
	# __init__()

	def setData( self, data ):
		self.data = bytes(data)
	# setData

	def send( self ):
		return self.canBus.sendMsg( self )
	# send()

# end class can
