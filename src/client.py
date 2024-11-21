#!/usr/bin/env python3
"""
JSON-RPC 2.0 Client implementation with class-based RPC support
"""
from jsonrpclib import Server
from typing import Any


class RPCProxy:
    """Proxy class to handle method calls for a specific class"""
    def __init__(self, server_connection, class_name: str):
        self._server = server_connection
        self._class_name = class_name

    def __getattr__(self, method_name: str) -> Any:
        """Handle method calls by constructing the full method path"""
        if method_name.startswith('_'):
            raise AttributeError(f"Cannot access private method {method_name}")
        
        # Construct the full method path (ClassName.method)
        method_path = f"{self._class_name}.{method_name}"
        
        # Return a lambda that will make the actual RPC call
        return lambda *args, **kwargs: getattr(self._server, method_path)(*args, **kwargs)


class RPCClient:
    def __init__(self, host="localhost", port=8080):
        """Initialize RPC client with host and port"""
        self.server = Server(f'http://{host}:{port}')
        
    def get_proxy(self, class_name: str) -> RPCProxy:
        """Get a proxy for a specific class"""
        return RPCProxy(self.server, class_name)


if __name__ == "__main__":
    # Example usage
    client = RPCClient()
    try:
        # Get a proxy for the Calculator class
        calc = client.get_proxy("Calculator")
        
        # Make RPC calls using natural object-oriented syntax
        result = calc.add(5, 3)
        print(f"5 + 3 = {result}")
        
        result = calc.subtract(10, 4)
        print(f"10 - 4 = {result}")
        
        result = calc.multiply(6, 7)
        print(f"6 * 7 = {result}")
    except ConnectionRefusedError:
        print("Error: Could not connect to RPC server. Make sure it's running.")
