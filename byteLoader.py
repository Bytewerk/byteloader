#!/usr/bin/python3
# -*- coding: utf-8 -*-

from sys import exit
#import time
#import math
from can import CanMsg
from enum import Enum
from time import sleep



if __name__ == "__main__":
	print( 'please run \'main.py\' instead' )
	exit( 0 )


states = Enum( 'states', 'RESET REQ_IDENT WAIT_IDENT_RESP SET_ADDR SEND_DATA ERROR EXIT' )



class ByteLoader( ):
	def __init__( self, canBus ):
		self.canBus = canBus
		self.canId = 0x133707FF
		self.fileData = []
		self.state = states.RESET

		self.boardId = 0xFF
		self.msgNumber = 0
		self.fMsgCounter = 0
		self.pageSize = 0
		self.pageCount = 0
	# end init


	def importHexFile( self, fileName ):
		with open( fileName, 'rb' ) as f:
			self.fileData = f.read( )
	# end importHexFile





	def run( self ):
		# protocol description see
		# http://www.kreatives-chaos.com/artikel/can-bootloader
		while True:
			sleep( 0.1 ) # seconds


			if self.state == states.RESET:
				print( 'state[RESET]' )
				self.msgNumber = 0
				self.fMsgCounter = 0
				print( '' )

				self.state = states.REQ_IDENT
				continue
			# end STATE RESET


			elif self.state == states.REQ_IDENT:
				print( 'state[REQ_IDENT]' )
				print( '    msgNumber =', self.msgNumber )

				ok = self.__requestIdentify( )
				if ok is False:
					print( 'ERROR: cannot send identification request' )
					return 1

				print( '' )
				self.state = states.WAIT_IDENT_RESP
				continue
			# end STATE REQUEST IDENTIFICATION


			if self.state == states.WAIT_IDENT_RESP:
				print( 'state[WAIT_IDENT_RESP]' )
				print( '' )

				ok = self.__receiveIdentify( )
				if ok is False:
					print('ERROR: no identification response' )
					return 2

				# waiting here might take a while.
				# The device might not be powered on already

				self.state = states.EXIT
				continue
			# end STATE RESET


			if self.state == states.EXIT:
				print( 'state[EXIT]' )
				return False
			# end STATE EXIT

			else:
				self.state = states.EXIT
			# end STOTE UNKNOWN
		# end mainLoop
	# end run



	def __requestIdentify( self ):
		txMsg = CanMsg( self.canBus, self.canId, True )
		print( '    > sending: Request to get Identification' )
		data = bytearray( )
		data.append( self.boardId ) # Board-ID
		data.append( 0x01 ) # Type = Request, Command = Identify
		data.append( self.msgNumber ) # iterates to spot missing messages
		data.append( 0x80 ) # SOB = 1, Following Msg Count = 0
		txMsg.setData( data )

		print( '    boardId=%d' % self.boardId )
		print( '    msgNum=%d' % self.msgNumber )
		print( '' )

		ok = txMsg.send( )
		if ok == True:
			print( 'ERROR: Cannot send msg' )
			return False
		else:
			return True
	# end __requestIdentify



	def __receiveIdentify( self ):
		print( '    > receiving: Identification response' )

		while True:
			rxMsg = self.canBus.getMsgNonBlocking( )

			if rxMsg == None:
				sleep( 0.1 )
				continue # TODO: timeout!

			if rxMsg.id != self.canId -1:
				continue # not a bootloader message

			if self.boardId != rxMsg.data[0]:
				print( '    ERROR: bootloader version does not match' )
				print( '    Expected: %d, got: %d' % (self.boardId, rxMsg.data[0]))
				return False

			self.pageSize = rxMsg.data[2]
			self.pageCount = rxMsg.data[3]
			print( '    data: bootloader =',        rxMsg.data[0] )
			print( '    data: bootloaderVersion =', rxMsg.data[1] )
			print( '    data: pageSize =',          rxMsg.data[2] )
			print( '    data: rwwPageCount =',      rxMsg.data[3] )

			return True
		# while True









#
#			if state == states.RESET:
#				print( 'state: RESET' )
#				print( '' )
#				msgCount = 0
#				dataOffset = 0
#
#				state = states.REQ_IDENT
#				continue
#			# end RESET
#
#			if state == states.REQ_IDENT:
#				print( 'state: REQUEST IDENTIFIER' )
#				print( '    msgCount =', msgCount )
#				print( '    dataOffset =', dataOffset )
#
#				s.settimeout( 0.2 ) # cram at least 2 msgs into the bootloader timeout(500ms)
#				if send_identifyRequest( s, msgCount ) is False:
#					sys.exit( 1 )
#					continue
#
#				print( '' )
#				state = states.GET_IDENT
#				continue
#			# end REQ_IDENT
#
#







#			elif state == states.GET_IDENT:
#				print( 'state: GET IDENTIFIER' )
#				data = canGetData( s )
#				if data == None: # Retry the whole thing
#					print( 'ERROR: got invalid data' )
#					print( '' )
#
#					state = states.RESET
#					continue
#
#				# parse
#				ident = parse_identifyResponse( data )
#				if ident == None:
#					print( 'ERROR: misparsed data' )
#					print( '' )
#
#					state = states.RESET
#					continue
#












#				print( '    data: bootloader =', ident[0] )
#				print( '    data: bootloaderVersion =', ident[1] )
#				print( '    data: pageSize =', ident[2] )
#				print( '    data: rwwPageCount =', ident[3] )
#				print( '' )
#
#				state = states.SET_ADDR
#				continue
#			# end GET IDENT
#
#
#			elif state == states.SET_ADDR: # Send SET_ADDRESS
#				print( 'state: SET ADDRESS' )
#				msgCount += 1
#				send_setAddress( s, ident[2], ident[3], dataOffset, msgCount )
#				data = canGetData( s )
#				if data is None:
#					print( 'ERROR: got invalid data' )
#					print( '' )
#
#					state = states.RESET
#					continue
#
#				ok = parse_ackResponse( data, 0x01, 0x02 ) # Type=Request, Cmd=SET_ADDRESS
#				fMsgCount = 0
#				if ok is not True:
#					print( 'ERROR: got invalid data' )
#					print( '' )
#
#					state = states.RESET
#					continue
#
#				print( 'ok' )
#				print( '' )
#				state = states.SEND_DATA
#			# end SET ADDR
#
#
#
#			elif state == states.SEND_DATA:
#				print( 'state: SEND DATA' )
#				# select the right 4 byte to send in this message
#				sendData = []
#				sendData.append( fileData[dataOffset + 0] )
#				sendData.append( fileData[dataOffset + 1] )
#				sendData.append( fileData[dataOffset + 2] )
#				sendData.append( fileData[dataOffset + 3] )
#				dataOffset += 4
#
#				msgCount += 1
#				#sock, sendData, pageSize, fMsgCnt, msgCount
#				send_flashData( s, sendData, ident[3], msgCount )
#
#				data = canGetData( s )
#				if data is None:
#					print( 'ERROR: got invalid data' )
#					print( '' )
#
#					state = states.RESET
#					continue
#
#				ok = parse_ackResponse( data, 0x01, 0x03 ) # Type=Request, Cmd=DATA
#				if ok is not True:
#					print( 'ERROR: got invalid data' )
#					print( '' )
#
#					state = states.RESET
#					continue
#
#				print( 'ok' )
#				state = states.SET_ADDR
#			# end SEND DATA
#
#			else:
#				print( 'ERROR: UNKNOWN STATE:', state )
#				print( 'reverting to 0' )
#				print( '' )
#
#				state = states.RESET
#				continue
#			# end UNKNOWN STATE
#		# end of state machine
#	# files open
## end main



#def build_can_frame( can_id, data ):
#    can_dlc = len( data )
#    data = data.ljust( 8, b'\x00' )
#    return struct.pack( can_frame_fmt, can_id, can_dlc, data )
##build_can_frame()
#
#
#
#def canGetData( sock ):
#	sock.settimeout( 10 ) #(seconds) give it more time to respond
#	try:
#		data, crap = sock.recvfrom( 1024 )
#	except socket.timeout:
#		print( 'ERROR: CAN Timeout' )
#		return None
#
#	canMsg = dissect_can_frame( data )
#	if canMsg[0] == bootloaderCanId -1: # bootloader responds 1 Id lower
#		return canMsg[2] # pass on the can data only
## canGetData()
#
#
#
#def dissect_can_frame( frame ):
#    can_id, can_dlc, data = struct.unpack( can_frame_fmt, frame )
#    return (can_id, can_dlc, data[:can_dlc])
## dissect_can_frame()
#
#
#
#def canSendData( sock, msgData ):
#	sock.settimeout( 2 ) #(seconds) give it more time to respond
#	try:
#		sock.send( build_can_frame(bootloaderCanId, msgData) )
#	except socket.error:
#		print( 'ERROR: Cannot Send CAN frame' )
#		exit( 2 )
#	return 1
## canSendData()





#
#def parse_identifyResponse( data ):
#	boardId = data[0]
#	msgType = data[1] >> 6
#	command = data[1] & 0x3F
#
#	# type=success, cmd=identify, boardId=hardcoded to 0xFF
#	if msgType != 1 or command != 0x01 or boardId != 0xFF:
#		print( 'ERROR: Wrong response from device')
#		print( 'msgType=0x{:02x}, command=0x{:02x}, boardId=0x{:02x}'.format(msgType, command, boardId) )
#		return None
#
#	bootloaderType = data[4] >> 4
#	bootloaderVersion = data[4] & 0x0F
#	pageSizeId = data[5]
#	rwwPageCount = (data[6] << 8) + data[7]
#
#	if pageSizeId == 0:
#		pageSize = 32 # byte
#	elif pageSizeId == 1:
#		pageSize = 64 # byte
#	elif pageSizeId == 2:
#		pageSize = 128 # byte
#	elif pageSizeId == 3:
#		pageSize = 256 # byte
#	else:
#		return None
#
#	return [bootloaderType, bootloaderVersion, pageSize, rwwPageCount]
## parse_IdentifyResponse()
#
#
#
#def parse_ackResponse( data, expType, expCmd ):
#	msgType = data[1] >> 6
#	command = data[1] & 0x3F
#	if expType != msgType or expCmd != command:
#		print( 'ERROR: Wrong response from device' )
#		print( 'msgType=0x{:02x}, command=0x{:02x}'.format(msgType, command) )
#		return False
#	else:
#		return True
## parse_identifyResponse()
#
#
#def send_setAddress( sock, pageSize, pageCount, dataOffset, msgCount):
#	flashPage = int(math.floor((dataOffset / pageSize)))
#	pageBufferPosition = int(math.floor((dataOffset - (flashPage * pageSize)) / 4))
#	print( '    flashPage =', flashPage )
#	print( '    pageBufferPosition =', pageBufferPosition )
#	msgData = bytearray( )
#	msgData.append( 0xFF ) # Board-ID
#	msgData.append( 0x02 ) # Type = Request, Command = SET_ADDRESS
#	msgData.append( msgCount ) # Msgcounter
#	msgData.append( 0x80 ) # SOB = 1, fmsgcounter = 0
#	msgData.append( flashPage >> 8 ) # bigEndian
#	msgData.append( flashPage & 0xFF )
#	msgData.append( pageBufferPosition >> 8 ) # bigEndian
#	msgData.append( pageBufferPosition & 0xFF )
#
#	canSendData( sock, msgData )
## send_setAddress()
#
#
#
#def send_flashData( sock, sendData, pageSize, msgCount ):
#	print( '    flashData = [0x{:02x}][0x{:02x}][0x{:02x}][0x{:02x}]'.format(
#		sendData[0], sendData[1], sendData[2], sendData[3])
#	)
#
#	if fMsgCount == ((pageSize / 4) -1):
#		sob=0x80
#	else:
#		sob=0x00
#
#
#	# TODO: WHAT ABOUT ENDIANESS ?!
#	msgData = bytearray( )
#	msgData.append( 0xFF )      # Board-ID
#	msgData.append( 0x03 )      # Type = Request, Command = DATA
#	msgData.append( msgCount )  # global Msgcounter
#	msgData.append( sob + fMsgCount&0x7F )
#	msgData.append( sendData[0] )
#	msgData.append( sendData[1] )
#	msgData.append( sendData[2] )
#	msgData.append( sendData[3] )
#	canSendData( sock, msgData )
#	print( '' )
## send_dataRequest()
