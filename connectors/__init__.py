import socket


class SocketConn:
    buffer_size = 1024*4

    def __init__(self, hostname, port):
        self._hostname = hostname
        self._port = port
        self._socket = None
        self._conn = None
        self.operator = None

    def start_connection(self):
        address = (self._hostname, self._port)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(address)
            print("Connected to address:", socket.gethostbyname(socket.gethostname()) + ":" + str(self._port))
            self._socket = s
            self.operator = self._socket
        except OSError as e:
            raise OSError("Error while connecting :: %s" % e)

    def close(self):
        self._socket.close()
        self._socket = None


class SocketServerConn(SocketConn):
    def start_connection(self):
        address = (self._hostname, self._port)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(address)
            s.listen(5)
            print("Connected to address:", socket.gethostbyname(socket.gethostname()) + ":" + str(self._port))
            self._socket = s
            self._conn, _ = self._socket.accept()
            self.operator = self._conn
        except OSError as e:
            raise OSError("Error while connecting :: %s" % e)

    def close(self):
        self._socket.close()
        self._socket = None
        self._conn.close()
        self._conn = None


class ConnectionNotFound(Exception):
    pass

class SocketClient:
    def __init__(self, conn: SocketConn):
        self.conn = conn

    def start(self):
        self.conn.start_connection()

    def stop(self):
        self.conn.close()

    def read(self, byteLength=None):
        if not self.conn.operator:
            raise ConnectionNotFound('No connection')
        return self.conn.operator.recv(byteLength or self.conn.buffer_size)

    def write(self, msg: str):
        try:
            self.conn.operator.send(bytes(msg, "utf-8"))
        except socket.error as e:
            raise ConnectionNotFound("error while sending :: " + str(e))

    def write_all(self, msg: str):
        try:
            self.conn.operator.sendall(bytes(msg, "utf-8"))
        except socket.error as e:
            raise ConnectionNotFound("error while sending :: " + str(e))
