import socket


class WOLNetworkInteract:
    """Class that provides tools for working with Wake-On-LAN payload data and network transmission."""
    @staticmethod
    def pack_data(mac_address):
        """Turns a MAC address into required bytes for WOL."""
        return 6 * bytes.fromhex('FF') + 16 * mac_address  ## Didn't work initially because I passed the payload as a byte-encoded string, not hex-encoded bytes

    @staticmethod
    def broadcast(message: bytes = b"OwO what's this? A test?"):  ## I was bored sorry
        """Broadcasts bytes to all devices on connected network."""
        socket.gethostbyname(socket.gethostname())
        ## Create a datagram mode socket...
        connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  ## Didn't work initially because I didn't know it had to be a datagram
        ## set it to broadcast mode...
        connection.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        ## and broadcast the message.
        connection.sendto(message, ('255.255.255.255', 7))  ## 255.255.255.255 is all hosts on network


if __name__ == '__main__':
    ## Demonstrate broadcasting.
    WOLNetworkInteract.broadcast()
    ## Wake something
    #WOLNetworkInteract.broadcast(WOLNetworkInteract.pack_data(bytes.fromhex('24418C644DC6')))
