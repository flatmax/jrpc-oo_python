#!/usr/bin/env python3
"""
JSON-RPC 2.0 Server implementation with WebSocket support
"""
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import inspect
import json
import asyncio
import websockets
from urllib.parse import urlparse
import traceback


class RPCServer:
    def __init__(self, host='localhost', port=8080):
        """Initialize WebSocket RPC server"""
        self.host = host
        self.port = port
        self.instances = {}
        self._system_methods = {
            'system.listComponents': self.list_components
        }
        print("RPC Server initialized")

    def list_components(self):
        """List all registered components and their methods
        This is called by jrpc-oo's setupRemote to discover available instances and methods
        Returns a dictionary of method names in the format {class_name.method_name: True}
        """
        print('list components')
        components = {}
        for class_name, instance in self.instances.items():
            for name, method in inspect.getmembers(instance, inspect.ismethod):
                if not name.startswith('_'):  # Only include public methods
                    method_name = f"{class_name}.{name}"
                    components[method_name] = True
        
        print(components)
        return components

    def register_instance(self, instance, class_name=None):
        """Register a class instance for RPC access"""
        if class_name is None:
            class_name = instance.__class__.__name__
        
        self.instances[class_name] = instance

    async def _handle_ws_message(self, websocket, message):
        """Handle incoming WebSocket message"""
        print(f"\nReceived WebSocket message: {message}")
        try:
            # Parse message as JSON-RPC
            parsed = json.loads(message)
            print(f"Parsed JSON-RPC message: {parsed}")

            # Get method name and parameters
            method_name = parsed.get('method')
            params = parsed.get('params', {})
            
            # Extract args from params if present
            if isinstance(params, dict) and 'args' in params:
                args = params['args']
            else:
                args = params if isinstance(params, list) else [params]
                
            print(f"Method: {method_name}, Args: {args}")

            # Handle system methods first
            if method_name in self._system_methods:
                print(f"Calling system method: {method_name}")
                result = self._system_methods[method_name]()
                print(f"System method result: {result}")
                response = json.dumps({
                    'jsonrpc': '2.0',
                    'result': result,
                    'id': parsed.get('id')
                })
            # Handle instance methods
            elif '.' in method_name:
                class_name, method = method_name.split('.')
                instance = self.instances.get(class_name)
                if instance and hasattr(instance, method):
                    print(f"Found method {method} in class {class_name}")
                    method_obj = getattr(instance, method)
                    result = await asyncio.get_event_loop().run_in_executor(None, method_obj, *args)
                    print(f"Method result: {result}")
                    response = json.dumps({
                        'jsonrpc': '2.0',
                        'result': result,
                        'id': parsed.get('id')
                    })
                else:
                    print(f"Method {method_name} not found")
                    response = json.dumps({
                        'jsonrpc': '2.0',
                        'error': {'code': -32601, 'message': f'Method {method_name} not found'},
                        'id': parsed.get('id')
                    })
            else:
                print(f"Invalid method name format: {method_name}")
                response = json.dumps({
                    'jsonrpc': '2.0',
                    'error': {'code': -32601, 'message': f'Invalid method name format: {method_name}'},
                    'id': parsed.get('id')
                })

            print(f"Sending response: {response}")
            await websocket.send(response)

        except Exception as e:
            print(f"Error handling message: {str(e)}")
            print(f"Error traceback: {traceback.format_exc()}")
            error_response = json.dumps({
                'jsonrpc': '2.0',
                'error': {'code': -32603, 'message': str(e)},
                'id': parsed.get('id') if 'parsed' in locals() else None
            })
            print(f"Sending error response: {error_response}")
            await websocket.send(error_response)

    async def _handle_ws_connection(self, websocket):
        """Handle WebSocket connection"""
        try:
            async for message in websocket:
                await self._handle_ws_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
        except Exception as e:
            print(f"Error in WebSocket handler: {str(e)}")

    async def serve(self):
        """Start the WebSocket server"""
        # Print registered methods
        print(f"\nRegistered classes and methods:")
        for class_name, instance in self.instances.items():
            print(f"\n{class_name}:")
            for name, method in inspect.getmembers(instance, inspect.ismethod):
                if not name.startswith('_'):
                    print(f"  - {name}")

        # Create and start WebSocket server
        self.ws_server = await websockets.serve(
            self._handle_ws_connection,
            self.host,
            self.port,
            subprotocols=['jsonrpc']  # Specify JSON-RPC subprotocol
        )
        print(f"WebSocket server running on ws://{self.host}:{self.port}")
        await self.ws_server.wait_closed()

    def shutdown(self):
        """Shutdown the server"""
        if self.ws_server:
            self.ws_server.close()


# Example class for testing
class Calculator:
    """A simple calculator class for testing RPC"""
    
    def add(self, a, b):
        """Add two numbers"""
        print(f'Calculator.add called with: a={a}, b={b}')
        result = a + b
        print(f'Calculator.add result: {result}')
        return result

    def subtract(self, a, b):
        """Subtract b from a"""
        print(f'Calculator.subtract called with: a={a}, b={b}')
        result = a - b
        print(f'Calculator.subtract result: {result}')
        return result

    def multiply(self, a, b):
        """Multiply two numbers"""
        print(f'Calculator.multiply called with: a={a}, b={b}')
        result = a * b
        print(f'Calculator.multiply result: {result}')
        return result


if __name__ == "__main__":    
    # Create server
    server = RPCServer()
    
    # Register calculator instance
    calc = Calculator()
    server.register_instance(calc)
    
    try:
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()
