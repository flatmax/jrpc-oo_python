#!/usr/bin/env python3
"""
JSON-RPC 2.0 Server implementation with class-based RPC support
"""
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import inspect
import json
import asyncio
import websockets
import threading
from urllib.parse import urlparse


class RPCServer:
    def __init__(self, uri="http://localhost:8080"):
        """Initialize RPC server with URI
        URI can be either http://host:port or ws://host:port
        """
        self.uri = uri
        parsed = urlparse(uri)
        self.host = parsed.hostname or 'localhost'
        self.port = parsed.port or 8080
        self.protocol = parsed.scheme or 'http'
        
        self.instances = {}
        self.ws_server = None
        self.http_server = None
        
        # Register system methods
        self._register_system_methods()

    def _register_system_methods(self):
        """Register system methods including listComponents"""
        self._system_methods = {
            'system.listComponents': self.list_components
        }

    def list_components(self):
        """List all registered components and their methods
        This is called by jrpc-oo's setupRemote to discover available instances and methods
        Returns a dictionary of class names and their methods
        """
        components = {}
        for class_name, instance in self.instances.items():
            methods = []
            for name, method in inspect.getmembers(instance, inspect.ismethod):
                if not name.startswith('_'):  # Only include public methods
                    # Get method signature
                    sig = inspect.signature(method)
                    param_info = []
                    for param in sig.parameters.values():
                        if param.name != 'self':  # Skip self parameter
                            param_info.append({
                                'name': param.name,
                                'type': str(param.annotation) if param.annotation != inspect.Parameter.empty else 'any'
                            })
                    
                    methods.append({
                        'name': name,
                        'params': param_info,
                        'return': str(sig.return_annotation) if sig.return_annotation != inspect.Parameter.empty else 'any'
                    })
            
            components[class_name] = {
                'methods': methods,
                'doc': instance.__doc__ or ''
            }
        
        return components

    def register_instance(self, instance, class_name=None):
        """Register a class instance for RPC access"""
        if class_name is None:
            class_name = instance.__class__.__name__
        
        self.instances[class_name] = instance

    async def _handle_ws_message(self, websocket):
        """Handle WebSocket messages"""
        async for message in websocket:
            try:
                request = json.loads(message)
                method_path = request.get('method', '')
                params = request.get('params', [])
                request_id = request.get('id')

                # Handle system methods
                if method_path in self._system_methods:
                    result = self._system_methods[method_path]()
                else:
                    # Handle instance methods
                    class_name, method_name = method_path.split('.')
                    instance = self.instances.get(class_name)
                    if not instance:
                        raise Exception(f"Class {class_name} not found")
                    
                    method = getattr(instance, method_name, None)
                    if not method or method_name.startswith('_'):
                        raise Exception(f"Method {method_path} not found")
                    
                    result = method(*params)

                response = {
                    'jsonrpc': '2.0',
                    'result': result,
                    'id': request_id
                }
            except Exception as e:
                response = {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': -32000,
                        'message': str(e)
                    },
                    'id': request_id
                }

            await websocket.send(json.dumps(response))

    async def _start_ws_server(self):
        """Start WebSocket server"""
        async with websockets.serve(self._handle_ws_message, self.host, self.port):
            print(f"WebSocket server running on ws://{self.host}:{self.port}")
            await asyncio.Future()  # run forever

    def _start_http_server(self):
        """Start HTTP server"""
        self.http_server = SimpleJSONRPCServer((self.host, self.port))
        self.http_server.allow_reuse_address = True

        # Register all instance methods
        for class_name, instance in self.instances.items():
            for name, method in inspect.getmembers(instance, inspect.ismethod):
                if not name.startswith('_'):
                    method_path = f"{class_name}.{name}"
                    self.http_server.register_function(method, method_path)

        # Register system methods
        for method_path, method in self._system_methods.items():
            self.http_server.register_function(method, method_path)

        print(f"HTTP server running on http://{self.host}:{self.port}")
        self.http_server.serve_forever()

    def serve_forever(self):
        """Start the server based on protocol"""
        print(f"\nRegistered classes and methods:")
        for class_name, instance in self.instances.items():
            print(f"\n{class_name}:")
            for name, method in inspect.getmembers(instance, inspect.ismethod):
                if not name.startswith('_'):
                    print(f"  - {name}")

        if self.protocol == 'ws':
            asyncio.run(self._start_ws_server())
        else:
            self._start_http_server()

    def shutdown(self):
        """Shutdown the server"""
        if self.http_server:
            self.http_server.shutdown()
            self.http_server.server_close()


# Example class for testing
class Calculator:
    """A simple calculator class for testing RPC"""
    
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
    import sys
    
    # Default to HTTP if no protocol specified
    uri = "ws://localhost:8080" if len(sys.argv) > 1 and sys.argv[1] == "ws" else "http://localhost:8080"
    
    server = RPCServer(uri)
    calc = Calculator()
    server.register_instance(calc)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
