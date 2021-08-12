from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.topo import Topo

class red2(Topo):
    def __init__(self):
        Topo.__init__(self)

        #info( '*** Anadiendo hosts\n' )
        h1 = self.addHost('h1', mac = "00:00:00:00:00:01")
        h2 = self.addHost('h2', mac = "00:00:00:00:00:02")
        h3 = self.addHost('h3', mac = "00:00:00:00:00:03")
        h4 = self.addHost('h4', mac = "00:00:00:00:00:04")
        h5 = self.addHost('h5', mac = "00:00:00:00:00:05")
        h6 = self.addHost('h6', mac = "00:00:00:00:00:06")


        #info( '*** Anandiendo switches\n' )
        s1 = self.addSwitch('s1', dpid = '1')
        s2 = self.addSwitch('s2', dpid = '2')
        s3 = self.addSwitch('s3', dpid = '3')
        s4 = self.addSwitch('s4', dpid = '4')
        s5 = self.addSwitch('s5', dpid = '5')

        #info( '*** Creando links\n' )
        self.addLink(h1, s1, 1, 2)
        self.addLink(h2, s1, 3, 4)

        self.addLink(h3, s2, 5, 6)
        self.addLink(h4, s2, 7, 8)

        self.addLink(h5, s5, 9, 10)
        self.addLink(h6, s5, 11, 12)

        self.addLink(s1, s5, 13, 14)
        self.addLink(s5, s3, 15, 16)
        self.addLink(s3, s1, 17, 18)
        self.addLink(s3, s4, 19, 20)
        self.addLink(s4, s2, 21, 22)
        self.addLink(s2, s1, 23, 24)


topos = {'red2':(lambda:red2())}
