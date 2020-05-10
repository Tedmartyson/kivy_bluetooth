# import kivy module 
import kivy 

# Kivy Example App for the slider widget 
from kivy.app import App 

# The GridLayout arranges children in a matrix. 
from kivy.uix.gridlayout import GridLayout 

# If we will not import this module 
# It will through the error 
from kivy.uix.slider import Slider 

# The Label widget is for rendering text. 
from kivy.uix.label import Label
from kivy.uix.button import Button

from kivy.logger import Logger
from jnius import autoclass

# Property that represents a numeric value 
# within a minimum bound and / or maximum 
# bound – within a numeric range. 
from kivy.properties import NumericProperty

# class in which we are defining the 
# sliders and its effects 


class Bluetooth:
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
					self.UUID.fromString("00001105-0000-1000-8000-00805f9b34fb"))

				reader = self.InputStreamReader(socket.getInputStream(), 'US-ASCII')

				recv_stream = self.BufferedReader(reader)
				send_stream = socket.getOutputStream()
				break
		socket.connect()
		return recv_stream, send_stream



class WidgetContainer(GridLayout): 
	FONT_SIZE = '50'

	def __init__(self, recv_stream, send_stream, **kwargs):
		# super function can be used to gain access 
		# to inherited methods from a parent or sibling 
		# class that has been overwritten in a class object. 
		super(WidgetContainer, self).__init__(**kwargs) 

		self.recv_stream = recv_stream
		self.send_stream = send_stream

		# 4 cols in grid layout 
		self.rows = 4
		
		# declaring the slider and adding some effects to it 
		self.brightnessControl = Slider(min = 0, max = 100) 
		

		# 1st row - one label, one slider	 
		self.add_widget(Label(text ='brightness', font_size = self.FONT_SIZE)) 
		self.add_widget(self.brightnessControl) 

		# 2nd row - one label for caption, 
		# one label for slider value 
		self.add_widget(Label(text ='Slider Value', font_size = self.FONT_SIZE)) 
		self.brightnessValue = Label(text ='0', font_size = self.FONT_SIZE) 
		self.add_widget(self.brightnessValue) 


		# On the slider object Attach a callback 
		# for the attribute named value 
		self.brightnessControl.bind(value = self.on_value) 
		
	# Adding functionality behind the slider 
	# i.e when pressed increase the value 
	def on_value(self, instance, brightness): 
		self.brightnessValue.text = "% d"% brightness
		self.send_stream.write(f'{brightness}'.encode())
		print(f'brightness: {brightness}')
		self.send_stream.flush()
		
# The app class 
class SliderExample(App):

	bluetooth = Bluetooth('ilya-Vostro-15-3568')
	def build(self):
		recv_stream, send_stream = self.bluetooth.get_socket_stream()
		widgetContainer = WidgetContainer(recv_stream, send_stream) 
		return widgetContainer 


# creating the object root for ButtonApp() class 
root = SliderExample() 
	
# run function runs the whole program 
# i.e run() method which calls the 
# target function passed to the constructor. 
root.run() 
