import pytest
from unittest.mock import MagicMock
from connectors import SocketConn, SocketServerConn, SocketClient, ConnectionNotFound
from socket import error as socketError


def test_socket_connection():
    conn = SocketConn('foo', '9999')
    conn.start_connection = MagicMock()
    conn.close = MagicMock()
    conn.operator = MagicMock()
    conn.operator.recv = MagicMock()
    conn.operator.send = MagicMock()
    conn.operator.sendall = MagicMock()

    sc = SocketClient(
        conn
    )
    sc.start()
    conn.start_connection.assert_called_once()

    sc.read(byteLength=1012)
    conn.operator.recv.assert_called_once_with(1012)

    sc.write('hello world')
    conn.operator.send.assert_called_once_with(bytes('hello world', 'utf-8'))

    sc.write_all('hello world')
    conn.operator.sendall.assert_called_once_with(bytes('hello world', 'utf-8'))

    sc.stop()
    conn.close.assert_called_once()


def test_socket_connection_connection_error():
    conn = SocketConn('foo', '9999')
    conn.start_connection = MagicMock(side_effect=OSError("Error while connecting :: DUMMY ERROR"))
    conn.close = MagicMock()
    conn.operator = MagicMock()
    conn.operator.recv = MagicMock()
    conn.operator.send = MagicMock(side_effect=socketError("dummy error 1"))
    conn.operator.sendall = MagicMock(side_effect=socketError("dummy error 2"))

    sc = SocketClient(
        conn
    )
    with pytest.raises(OSError):
        sc.start()

    with pytest.raises(ConnectionNotFound):
        sc.write('hello world')

    with pytest.raises(ConnectionNotFound):
        sc.write_all('hello world')


def test_socket_server_connection():
    conn = SocketServerConn('foo', '9999')
    conn.start_connection = MagicMock()
    conn.close = MagicMock()
    conn.operator = MagicMock()
    conn.operator.recv = MagicMock()
    conn.operator.send = MagicMock()
    conn.operator.sendall = MagicMock()

    sc = SocketClient(
        conn
    )
    sc.start()
    conn.start_connection.assert_called_once()

    sc.read(byteLength=1012)
    conn.operator.recv.assert_called_once_with(1012)

    sc.write('hello world')
    conn.operator.send.assert_called_once_with(bytes('hello world', 'utf-8'))

    sc.write_all('hello world')
    conn.operator.sendall.assert_called_once_with(bytes('hello world', 'utf-8'))

    sc.stop()
    conn.close.assert_called_once()


def test_socket_server_connection_connection_error():
    conn = SocketServerConn('foo', '9999')
    conn.start_connection = MagicMock(side_effect=OSError("Error while connecting :: DUMMY ERROR"))
    conn.close = MagicMock()
    conn.operator = MagicMock()
    conn.operator.recv = MagicMock()
    conn.operator.send = MagicMock(side_effect=socketError("dummy error 1"))
    conn.operator.sendall = MagicMock(side_effect=socketError("dummy error 2"))

    sc = SocketClient(
        conn
    )
    with pytest.raises(OSError):
        sc.start()

    with pytest.raises(ConnectionNotFound):
        sc.write('hello world')

    with pytest.raises(ConnectionNotFound):
        sc.write_all('hello world')
