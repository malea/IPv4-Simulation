# IPv4 Router Simulation

**Requires Python 3.**

    python3 --version

To run part 1:

    python3 main.py < pdus.txt

(Files `routes.txt`, `arp.txt`, and `nat.txt` should be in current working
directory.)

To run part 2, you must use the environment variable `NP_PRJ1_PART_2`.

For example:

    NP_PRJ1_PART_2=1 ruby nat_test.rb "python3 main.py"
