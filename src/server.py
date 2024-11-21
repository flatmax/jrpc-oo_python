#!/usr/bin/env python3
"""
JSON-RPC 2.0 Server implementation with class-based RPC support
"""
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import inspect


class RPCServer:
    def __init__(self, host="localhost", port=8080):
        """Initialize RPC server with host and port"""
        self.server = SimpleJSONRPCServer((host, port))
        self.server.allow_reuse_address = True  # Allow reuse of address
        self.instances = {}

    def register_instance(self, instance, class_name=None):
        """Register a class instance for RPC access"""
        if class_name is None:
            class_name = instance.__class__.__name__
        
        self.instances[class_name] = instance
        
        # Register all public methods of the class
        for name, method in inspect.getmembers(instance, inspect.ismethod):
            if not name.startswith('_'):  # Only register public methods
                method_path = f"{class_name}.{name}"
                self.server.register_function(method, method_path)

    def serve_forever(self):
        """Start the server"""
        print(f"Server running on {self.server.server_address}")
        print("Registered classes and methods:")
        for class_name, instance in self.instances.items():
            print(f"\n{class_name}:")
            for name, method in inspect.getmembers(instance, inspect.ismethod):
                if not name.startswith('_'):
                    print(f"  - {name}")
        self.server.serve_forever()

    def shutdown(self):
        """Shutdown the server and cleanup resources"""
        self.server.shutdown()
        self.server.server_close()


# Example class for testing
class Calculator:
    def add(self, a: float, b: float) -> float:
        """Add two numbers"""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtract b from a"""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers"""
        return a * b


if __name__ == "__main__":
    server = RPCServer()
    calc = Calculator()
    server.register_instance(calc)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
