"""
Bluetooth class module
"""

# Module, which provides JavaClasses
from jnius import autoclass


class Bluetooth:

	UUID_string = '00001105-0000-1000-8000-00805f9b34fb'

	# Using adroid libs to get access to Bluetooth
	BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
	BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
	BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
	InputStreamReader = autoclass('java.io.InputStreamReader')
	BufferedReader = autoclass('java.io.BufferedReader')
	UUID = autoclass('java.util.UUID')

	def __init__(self, name):
		self.name = name

	def get_socket_stream(self):
		paired_devices = self.BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
		socket, recv_stream, send_stream = None, None, None
		for device in paired_devices:
			if device.getName() == self.name:
				socket = device.createRfcommSocketToServiceRecord(
					self.UUID.fromString(self.UUID_string))

				reader = self.InputStreamReader(socket.getInputStream(), 'US-ASCII')

				recv_stream = self.BufferedReader(reader)
				send_stream = socket.getOutputStream()
				break
		socket.connect()
		return recv_stream, send_stream
