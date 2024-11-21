#!/usr/bin/env python3
"""
Tests for JSON-RPC 2.0 implementation
"""
import pytest
import threading
import time
import socket
from src.server import RPCServer
from src.client import RPCClient


def find_free_port():
    """Find a free port to use for testing"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


@pytest.fixture
def server_port():
    """Get a free port for the server"""
    return find_free_port()


@pytest.fixture
def server(server_port):
    """Start a server instance for testing"""
    server = RPCServer(port=server_port)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.1)  # Give server time to start
    yield server
    server.server.server_close()  # Properly close the server
    time.sleep(0.1)  # Give time for the socket to be released


@pytest.fixture
def client(server_port):
    """Create a client instance for testing"""
    return RPCClient(port=server_port)


def test_add(server, client):
    """Test addition via RPC"""
    assert client.add(5, 3) == 8
    assert client.add(-1, 1) == 0
    assert client.add(0.5, 0.5) == 1.0


def test_subtract(server, client):
    """Test subtraction via RPC"""
    assert client.subtract(5, 3) == 2
    assert client.subtract(-1, 1) == -2
    assert client.subtract(0.5, 0.5) == 0.0


def test_multiply(server, client):
    """Test multiplication via RPC"""
    assert client.multiply(5, 3) == 15
    assert client.multiply(-2, 3) == -6
    assert client.multiply(0.5, 2) == 1.0
