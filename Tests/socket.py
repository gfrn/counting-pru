import socket
import unittest

port = 5000
host = "127.0.0.1"

def checksum(data:list) -> bool:
    csum = 0
    for i in data:
        csum += i

    return not (csum & 0xFF)

def include_checksum(list_values) -> list:
    counter = 0
    i = 0
    while i < len(list_values):
        counter += list_values[i]
        i += 1
    counter = counter & 0xff
    counter = (256 - counter) & 0xff
    return bytes(list_values + [counter])

class SocketTest(unittest.TestCase):

    def test_read(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, 5000))

        s.sendall(include_checksum([0x01, 0x10, 0x00, 0x01, 0x03]))
        data = s.recv(1024)
        s.close()

        self.assertEqual(data[1], 0x11)
        self.assertTrue(checksum(data))

    def test_timebase_write_redis(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, 5000))

        s.sendall(include_checksum([0x01, 0x20, 0x00, 0x00, 0x00, 0x00, 0x1e]))
        data = s.recv(1024)
        self.assertEqual(data[1], 0xe0)
        self.assertTrue(checksum(data))

        s.sendall(include_checksum([0x01, 0x10, 0x00, 0x00, 0x00]))
        data = s.recv(1024)

        self.assertEqual(data[5], 30)
        self.assertEqual(data[1], 0x11)
        self.assertTrue(checksum(data))

        s.sendall(include_checksum([0x01, 0x20, 0x00, 0x00, 0x00, 0x00, 0x3c]))
        data = s.recv(1024)
        self.assertEqual(data[1], 0xe0)
        self.assertTrue(checksum(data))

        s.sendall(include_checksum([0x01, 0x10, 0x00, 0x00, 0x00]))
        data = s.recv(1024)

        s.close()

        self.assertEqual(data[5], 60)
        self.assertEqual(data[1], 0x11)
        self.assertTrue(checksum(data))
        

    def test_serial_redis(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, 5000))

        # Writes serial no., then reads it back. 
        for i in range(1,9):
            s.sendall(include_checksum([0x01, 0x20, 0x00, 0x00, 0x0a + i, i]))
            data = s.recv(1024)

            self.assertTrue(checksum(data))
            self.assertEqual(data[1], 0xe0)

        for i in range(1,9):
            s.sendall(include_checksum([0x01, 0x10, 0x00, 0x00, 0x0a + i]))
            data = s.recv(1024)

            self.assertTrue(checksum(data))
            self.assertEqual(data[4], i)

        s.close()

    def test_group_read(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, 5000))

        s.sendall(include_checksum([0x01, 0x12, 0x00, 0x00, 0x01]))
        data = s.recv(1024)
        
        s.close()

        self.assertTrue(checksum(data))
        self.assertEqual(data[1], 0x13)

    def test_inhibit(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, 5000))

        s.sendall(include_checksum([0x01, 0x20, 0x00, 0x00, 0x09, 0x0c]))
        data = s.recv(1024)
        self.assertEqual(data[1], 0xe0)
        self.assertTrue(checksum(data))

        s.sendall(include_checksum([0x01, 0x10, 0x00, 0x00, 0x09]))
        data = s.recv(1024)
        self.assertEqual(data[1], 0x11)
        self.assertTrue(checksum(data))

        # Last two inhibits (LSB -> MSB) are 1
        self.assertEqual(data[4], 0x0c)

        s.sendall(include_checksum([0x01, 0x20, 0x00, 0x00, 0x09, 0x00]))
        data = s.recv(1024)
        self.assertEqual(data[1], 0xe0)
        self.assertTrue(checksum(data))

        s.sendall(include_checksum([0x01, 0x10, 0x00, 0x00, 0x09]))
        data = s.recv(1024)
        self.assertEqual(data[1], 0x11)
        self.assertTrue(checksum(data))

        s.close()

        # Inhibits back to 0
        self.assertEqual(data[4], 0x00)
        
unittest.main()

    


