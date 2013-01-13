#!/usr/bin/env python

import sys
import gtk
import appindicator

import netifaces
import subprocess

PING_FREQUENCY = 5

class OpenVPNInd:
	def __init__(self):
		self.ind = appindicator.Indicator("OpenVPN",
				"/home/ftoulemon/dev/openvpn_indicator/lock_ko.png",
				appindicator.CATEGORY_APPLICATION_STATUS)
		self.ind.set_status(appindicator.STATUS_ACTIVE)
		self.ind.set_attention_icon("/home/ftoulemon/dev/openvpn_indicator/lock_ok.png")
		
		self.p = subprocess.Popen('ls')

		self.menu_setup()
		self.ind.set_menu(self.menu)

	def menu_setup(self):
		self.menu = gtk.Menu()

		self.on_off_item = gtk.MenuItem("vpn on/off")
		self.on_off_item.connect("activate", self.switch)
		self.on_off_item.show()
		self.menu.append(self.on_off_item)

		self.quit_item = gtk.MenuItem("Quit")
		self.quit_item.connect("activate", self.quit)
		self.quit_item.show()
		self.menu.append(self.quit_item)
		
	def main(self):
		self.check_vpn()
		gtk.timeout_add(PING_FREQUENCY * 1000, self.check_vpn)
		gtk.main()

	def switch(self, widget):
		if self.p.poll() == None:
			self.p.terminate()
		else:
			self.p = subprocess.Popen(['/home/ftoulemon/vpn/vpn-alfred.sh',
				'80', 'tcp-client'])

	def quit(self, widget):
		sys.exit(0)

	def check_vpn(self):
		if 'tapVPN' in netifaces.interfaces():
			self.ind.set_status(appindicator.STATUS_ATTENTION)
		else:
			self.ind.set_status(appindicator.STATUS_ACTIVE)
		return True

if __name__== "__main__":
	indicator = OpenVPNInd()
	indicator.main()




