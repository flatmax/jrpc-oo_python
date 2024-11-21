#!/usr/bin/env python3
"""
Tests for JSON-RPC 2.0 implementation
"""
import pytest
import threading
import time
import socket
from src.server import RPCServer, Calculator
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
    calc = Calculator()
    server.register_instance(calc)
    
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(0.1)  # Give server time to start
    
    yield server
    
    server.shutdown()  # Properly shutdown the server
    server_thread.join(timeout=1)  # Wait for server thread to finish
    time.sleep(0.1)  # Give time for the socket to be released


@pytest.fixture
def calc_proxy(server_port):
    """Create a Calculator proxy for testing"""
    client = RPCClient(port=server_port)
    return client.get_proxy("Calculator")


def test_add(server, calc_proxy):
    """Test addition via RPC"""
    assert calc_proxy.add(5, 3) == 8
    assert calc_proxy.add(-1, 1) == 0
    assert calc_proxy.add(0.5, 0.5) == 1.0


def test_subtract(server, calc_proxy):
    """Test subtraction via RPC"""
    assert calc_proxy.subtract(5, 3) == 2
    assert calc_proxy.subtract(-1, 1) == -2
    assert calc_proxy.subtract(0.5, 0.5) == 0.0


def test_multiply(server, calc_proxy):
    """Test multiplication via RPC"""
    assert calc_proxy.multiply(5, 3) == 15
    assert calc_proxy.multiply(-2, 3) == -6
    assert calc_proxy.multiply(0.5, 2) == 1.0


def test_private_method_access(server, calc_proxy):
    """Test that private methods cannot be accessed"""
    with pytest.raises(AttributeError):
        calc_proxy._private_method()
