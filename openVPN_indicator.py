#!/usr/bin/env python

import sys
import gtk
import appindicator

import netifaces
import subprocess

PING_FREQUENCY = 5
port = '80'

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

		self.configm = gtk.Menu()
		self.config = gtk.MenuItem("Config")
		self.config.show()
		self.config.set_submenu(self.configm)
		self.port80 = gtk.CheckMenuItem("port 80")
		self.port80.set_active(True)
		self.port1194 = gtk.CheckMenuItem("port 1194")
		self.port80.connect("activate", self.port_select_80)
		self.port1194.connect("activate", self.port_select_1194)
		self.port80.show()
		self.port1194.show()
		self.configm.append(self.port80)
		self.configm.append(self.port1194)
		self.menu.append(self.config)

		self.separator = gtk.SeparatorMenuItem()
		self.separator.show()
		self.menu.append(self.separator)

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

	def port_select_80(self, widget):
		port = '80'
		self.port1194.set_active(False)

	def port_select_1194(self, widget):
		port = '1194'
		self.port80.set_active(False)

	def vpn_on(self, widget):
		self.p = subprocess.Popen(['/home/ftoulemon/vpn/vpn-alfred.sh',
			port, 'tcp-client'])
		self.vpn_off_item.show()
		self.vpn_on_item.hide()

	def vpn_off(self, widget):
		subprocess.call(['gksu', 'killall', 'openvpn'])
		self.vpn_off_item.hide()
		self.vpn_on_item.show()

	def quit(self, widget):
		sys.exit(0)

	def check_vpn(self):
		if 'tapVPN' in netifaces.interfaces():
			self.ind.set_status(appindicator.STATUS_ATTENTION)
			self.vpn_off_item.show()
			self.vpn_on_item.hide()
		else:
			self.ind.set_status(appindicator.STATUS_ACTIVE)
			self.vpn_off_item.hide()
			self.vpn_on_item.show()
		return True

if __name__== "__main__":
	indicator = OpenVPNInd()
	indicator.main()




