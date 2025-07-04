#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2')
    h3 = net.addHost('h3', cls=Host, ip='10.240.240.11')

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h1, s2, params1={ 'ip' : '10.100.100.1/24' })
    net.addLink(h2, s1)
    net.addLink(h2, s2, params1={ 'ip' : '10.100.100.2/24' } )
    net.addLink(h2, s3, params1={ 'ip' : '10.240.240.10/24' })
    net.addLink(h3, s3)

    net.build()

    info( '*** Configure VRF ***' )
    net['h1'].cmd('ip link add vrf1 type vrf table wan0 && ip link set dev vrf1 up')
    net['h2'].cmd('ip link add vrf1 type vrf table wan0 && ip link set dev vrf1 up')
    net['h1'].cmd('ip link set dev h1-eth1 master vrf1')
    net['h2'].cmd('ip link set dev h2-eth1 master vrf1')


    info( '*** Starting network\n')
    net.start()

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()