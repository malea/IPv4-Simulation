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

def create_arp_table(table):
    arp_table = {}
    for address, mac in table:
        arp_table[address] = mac
    return arp_table

def main(argv):
    routes = argv[1] if len(argv) > 1 else 'routes.txt'
    arp    = argv[2] if len(argv) > 2 else 'arp.txt'
    nat    = argv[3] if len(argv) > 3 else 'nat.txt'

    routing_table = create_routing_trie(read_table(routes))
    arp_table = create_arp_table(read_table(arp))
if __name__ == '__main__':
    main(sys.argv)
