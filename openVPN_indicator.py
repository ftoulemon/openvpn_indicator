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
		
		self.p = subprocess.Popen(['echo', 'vpn-alfred'])

		self.menu_setup()
		self.ind.set_menu(self.menu)

	def menu_setup(self):
		self.menu = gtk.Menu()

		self.vpn_on_item = gtk.MenuItem("vpn on")
		self.vpn_on_item.connect("activate", self.vpn_on)
		self.menu.append(self.vpn_on_item)

		self.vpn_off_item = gtk.MenuItem("vpn off")
		self.vpn_off_item.connect("activate", self.vpn_off)
		self.menu.append(self.vpn_off_item)

		self.quit_item = gtk.MenuItem("Quit")
		self.quit_item.connect("activate", self.quit)
		self.quit_item.show()
		self.menu.append(self.quit_item)

		if 'tapVPN' in netifaces.interfaces():
			self.vpn_off_item.show()
		else:
			self.vpn_on_item.show()
			
		
	def main(self):
		self.check_vpn()
		gtk.timeout_add(PING_FREQUENCY * 1000, self.check_vpn)
		gtk.main()

	def vpn_on(self, widget):
		self.p = subprocess.Popen(['/home/ftoulemon/vpn/vpn-alfred.sh',
			'80', 'tcp-client'])
		self.vpn_off_item.show()

	def vpn_off(self, widget):
		if self.p.poll() == None:
			self.p.terminate()
		else:
			subprocess.call(['gksu', 'killall', 'openvpn'])
		self.vpn_on_item.show()

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




