#!/usr/bin/env python3
"""
JSON-RPC 2.0 Server implementation
"""
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer


class RPCServer:
    def __init__(self, host="localhost", port=8080):
        """Initialize RPC server with host and port"""
        self.server = SimpleJSONRPCServer((host, port))
        self._register_methods()

    def _register_methods(self):
        """Register RPC methods"""
        self.server.register_function(self.add)
        self.server.register_function(self.subtract)
        self.server.register_function(self.multiply)

    def add(self, a: float, b: float) -> float:
        """Add two numbers"""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a"""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers"""
        return a * b

    def serve_forever(self):
        """Start the server"""
        print(f"Server running on {self.server.server_address}")
        self.server.serve_forever()


if __name__ == "__main__":
    server = RPCServer()
    server.serve_forever()
