import os
import sys
import collections

RouteValue = collections.namedtuple('RouteValue', ['destination', 'interface'])

class TrieNode(object):

    def __init__(self, parent):
        self.one = None
        self.zero = None
        self.value = None
        self.parent = parent

class Trie(object):

    def __init__(self):
        self.root = TrieNode(None)

    def put(self, prefix, value):
        """Add an entry to the trie.

        prefix - a string of zeros and ones as the prefix
        value - the value to store in the trie

        """
        node = self.root
        for bit in prefix:
            if bit == '1':
                if not node.one:
                    node.one = TrieNode(node)
                node = node.one
            elif bit == '0':
                if not node.zero:
                    node.zero = TrieNode(node)
                node = node.zero
            else:
                raise ValueError('invalid prefix')
        node.value = value

    def get(self, key):
        node = self.root
        for bit in key:
            if bit == '1':
                if not node.one:
                    break
                node = node.one
            elif bit == '0':
                if not node.zero:
                    break
                node = node.zero
            else:
                raise ValueError('invalid prefix')
        # if we're on a dead branch, check if a parent has a value
        while node.parent and not node.value:
            node = node.parent
        return node.value

def ip_to_binary_string(ip_address):
    parts = ip_address.split('.')
    return ''.join('{:0=8b}'.format(int(part)) for part in parts)

def cidr_to_binary_string(cidr_prefix):
    ip_address, bits = cidr_prefix.split('/')
    ip_string = ip_to_binary_string(ip_address)
    return ip_string[:int(bits)]

def read_table(path):
    with open(path) as table_file:
        for raw_line in table_file:
            line = raw_line.strip()
            if line:
                yield tuple(line.split())

def create_routing_trie(table):
    trie = Trie()
    for prefix, gateway, interface in table:
        binary_prefix = cidr_to_binary_string(prefix)
        value = RouteValue(gateway, interface)
        trie.put(binary_prefix, value)
    return trie

def simulate(routes, arp, nat, part_two=False):
    translations = {}
    while True:

        try:
            line = input()
        except EOFError:
            break
        (interface, source, destination, protocol, ttl_str, source_port,
                destination_port) = tuple(line.strip().split())

        ttl = int(ttl_str) - 1
        if ttl <= 0:
            print('{}:{}->{}:{} discarded (TTL expired)'.format(
                source, source_port,
                destination, destination_port,
            ))
            continue

        if part_two:
            key = (source, destination_port)
            if key in translations:
                # undo NAT translation on incoming packet
                destination, destination_port = translations[key]

        route = routes.get(ip_to_binary_string(destination))
        if not route:
            # should never happen with a default route
            print('Unreachable') # TODO: format
        next_hop = route.destination
        next_interface = route.interface

        if next_hop == '0.0.0.0':
            connection = 'directly connected '
            # if direct connection, ARP for the destination
            next_hop = destination
        else:
            connection = 'via ' + next_hop

        if next_interface.startswith('ppp'):
            dashmac = ''
        else:
            # only arp for non-ppp interface
            dashmac = '-' + arp[next_hop]

        if part_two:
            if next_interface in nat:
                next_port = source_port
                key = (destination, next_port)
                if key in translations:
                    next_port = '20000'
                    key = (destination, next_port)
                while key in translations:
                    next_port = str(int(next_port) + 1)
                    key = (destination, next_port)
                translations[key] = (source, source_port)
                # perform NAT translation on outgoing packet
                source = nat[next_interface]
                source_port = next_port

        print('{}:{}->{}:{} {}({}{}) ttl {}'.format(
            source, source_port,
            destination, destination_port,
            connection,
            next_interface,
            dashmac,
            ttl,
        ))

def main(argv):
    routes   = argv[1] if len(argv) > 1 else 'routes.txt'
    arp      = argv[2] if len(argv) > 2 else 'arp.txt'
    nat      = argv[3] if len(argv) > 3 else 'nat.txt'
    part_two = os.getenv('NP_PRJ1_PART_2') # could be a flag, I guess

    routing_table = create_routing_trie(read_table(routes))
    arp_table = dict(read_table(arp))
    nat_table = dict(read_table(nat))

    simulate(routing_table, arp_table, nat_table, part_two)

if __name__ == '__main__':
    main(sys.argv)
