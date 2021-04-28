import socket
from time import sleep
import unittest
import redis

r = redis.Redis(host="10.0.6.38")


def checksum(data: list) -> bool:
    csum = 0
    for i in data:
        csum += i

    print(csum)

    return not (csum & 0xff)


class SocketTest(unittest.TestCase):
    def test_read(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.0.6.38", 5000))

        s.sendall(b"\x01\x10\x00\x01\x03\xeb")
        data = s.recv(1024)
        s.close()

        self.assertTrue(checksum(data))
        self.assertEqual(data[1], 0x11)
        self.assertEqual(data[0], 0x00)

    def test_timebase_write_redis(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.0.6.38", 5000))

        s.sendall(b"\x01\x20\x00\x00\x00\x00\x3b\xa4")
        data = s.recv(1024)

        print(data)

        s.close()

        self.assertTrue(checksum(data))
        self.assertEqual(r.get("TimeBase"), b"59")


unittest.main()
