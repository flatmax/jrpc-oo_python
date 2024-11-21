#!/usr/bin/env python3
"""
JSON-RPC 2.0 Client implementation
"""
from jsonrpclib import Server


class RPCClient:
    def __init__(self, host="localhost", port=8080):
        """Initialize RPC client with host and port"""
        self.server = Server(f'http://{host}:{port}')

    def add(self, a: float, b: float) -> float:
        """Add two numbers using RPC"""
        return self.server.add(a, b)

    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a using RPC"""
        return self.server.subtract(a, b)

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers using RPC"""
        return self.server.multiply(a, b)


if __name__ == "__main__":
    # Example usage
    client = RPCClient()
    try:
        result = client.add(5, 3)
        print(f"5 + 3 = {result}")
        
        result = client.subtract(10, 4)
        print(f"10 - 4 = {result}")
        
        result = client.multiply(6, 7)
        print(f"6 * 7 = {result}")
    except ConnectionRefusedError:
        print("Error: Could not connect to RPC server. Make sure it's running.")
