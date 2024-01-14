#! /usr/bin/python3
import sys
import re

from network import WOLNetworkInteract
import storage


def magic_on_help():
    print('''Tool for waking up computers on a LAN using Wake-On-LAN. Computer's BIOSes must be set up to allow this.

Usage:
    magic_on.py -h|--help                     : Displays this message.
    magic_on.py -s|--send [MAC address|name]  : Send a WOL packet to the computer with [address] MAC address
                                                or send it to [name].
    magic_on.py -a|--add [MAC address] [name] : Add a computer entry to the program so [name] can be used
                                                instead of the MAC address.
    magic_on.py -d|--delete [name]            : Delete a computer's entry.''')


def send(arguments: list):
    """Send a WOL packet to the computer with the specified name or address."""
    database = storage.read_data()
    mac_address = re.compile(r'''((?:\d|[a-f]|[A-F]){2}):((?:\d|[a-f]|[A-F]){2}):((?:\d|[a-f]|[A-F]){2}):
                                 ((?:\d|[a-f]|[A-F]){2}):((?:\d|[a-f]|[A-F]){2}):((?:\d|[a-f]|[A-F]){2})''',
                             re.VERBOSE).fullmatch(arguments[1])

    ## Check if the input has an address stored in the database, and if it does, send the packet.
    if arguments[1] in database.keys():
        WOLNetworkInteract.broadcast(WOLNetworkInteract.pack_data(bytes.fromhex(database[arguments[1]])))
        print(f'WOL packet broadcast to {arguments[1]}.')

    ## If it's a MAC address, send it there.
    elif mac_address:
        hex_address = ''
        for digit in mac_address.groups():
            hex_address += digit
        WOLNetworkInteract.broadcast(WOLNetworkInteract.pack_data(bytes.fromhex(hex_address)))
        print(f'WOL packet broadcast for computer with MAC address {arguments[1]}.')

    ## We don't know what it was.
    else:
        print('Invalid MAC address (Should look like this: 1A:2B:3C:4D:5E:6F) or computer not stored.')


def add(arguments):  ## Arguments will contain a list, like this: ['--add', 'A1:B2:C3:D4:E5:F6', 'Computer Name']
    address_format = r'((?:\d|[a-f]|[A-F]){2})(?:\:)((?:\d|[a-f]|[A-F]){2})(?:\:)((?:\d|[a-f]|[A-F]){2})(?:\:)((?:\d|[a-f]|[A-F]){2})(?:\:)((?:\d|[a-f]|[A-F]){2})(?:\:)((?:\d|[a-f]|[A-F]){2})'
    regex_pattern = re.compile(address_format)
    result = regex_pattern.fullmatch(arguments[1])

    mac_dictionary = storage.read_data()

    if result:
        mac_string = ''
        count = 0
        mac_address_chunks = result.groups()
        while count != 6:
            mac_string += mac_address_chunks[count]
            count += 1
        storage.add_data(mac_dictionary, arguments[2], mac_string)

    else:
        print ('There is no viable MAC address that can be added.')


def delete(arguments: list):
    mac_dictionary = storage.read_data()
    if arguments[-1] in mac_dictionary:
        storage.delete_data(mac_dictionary, arguments[-1])
        print(f'{arguments[1]} was deleted.')
    else:
        print(f'{arguments[-1]} was misspelled or not stored')


if __name__ == '__main__':
    #if len(sys.argv) == 1 or sys.argv[1] in ('-h', '--help'):
    #    magic_on_help()
    #    exit(1)
    if len(sys.argv) > 1:
        if sys.argv[1] in ('-s', '--send') and len(sys.argv) == 3:
            send(sys.argv[1:])
        elif sys.argv[1] in ('-a', '--add') and len(sys.argv) == 4:
            add(sys.argv[1:])
        elif sys.argv[1] in ('-d', '--delete') and len(sys.argv) == 3:
            delete(sys.argv[1:])
        else:
            magic_on_help()
            exit(1)
    else:
        magic_on_help()
        exit(1)
