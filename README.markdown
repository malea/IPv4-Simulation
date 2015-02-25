# IPv4 Router Simulation

## Instructions for Use

To run:

    python3 main.py routes.txt arp.txt nat.txt < pdu.txt

###  `routes.txt`

Each line of this file represents a routing table entry. The table will have three whitespace 
deliminated columns.

1. IPv4 prefix in format `a.b.c.d/x`. [CIDR notation](http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing)
2. IPv4 gateway address in `a.b.c.d` notation.
3. Interface identifier: eth0, eth1, ppp0

Note: If the gateway address is 0.0.0.0 and the prefix length is 32, this indicates a direct, point-to-point connection.

### `arp.txt`

This file is used to create a dictionary that will simulate the "neighbor shouting" of ARP.
