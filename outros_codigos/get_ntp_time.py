import time

def gettime_ntp(addr='0.us.pool.ntp.org'):
    # http://code.activestate.com/recipes/117211-simple-very-sntp-client/
    import socket
    import struct
    import sys
    import time
    TIME1970 = 2208988800      # Thanks to F.Lundh
    client = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
    data = ('\x1b' + 47 * '\0').encode()
    client.sendto( data, (addr.encode(), 123))
    data, address = client.recvfrom( 1024 )
    if data:
        t = struct.unpack( '!12I', data )[10]
        t -= TIME1970
        return t
#
# def timestamp2datestring(timestamp,format="%a %b %d %X %Z %Y"):
#     return time.strftime(format,  time.gmtime(timestamp/1000.))
#
#
# def timestamp3datestring(timestamp):
#     return time.strftime(format,  time.gmtime(timestamp/1000.))

print(gettime_ntp("0.us.pool.ntp.org"))
time.sleep(2)
print(gettime_ntp())
print("terminou")
