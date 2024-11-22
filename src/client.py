#!/usr/bin/env python3
"""
JSON-RPC 2.0 Client implementation with WebSocket support and class-based RPC
"""
import json
import asyncio
import websockets
from typing import Any


class RPCProxy:
    """Proxy class to handle method calls for a specific class"""
    def __init__(self, client, class_name: str):
        self._client = client
        self._class_name = class_name

    def __getattr__(self, method_name: str) -> Any:
        """Handle method calls by constructing the full method path"""
        if method_name.startswith('_'):
            raise AttributeError(f"Cannot access private method {method_name}")
        
        # Construct the full method path (ClassName.method)
        method_path = f"{self._class_name}.{method_name}"
        
        # Return a lambda that will make the actual RPC call
        return lambda *args: self._client.call_method(method_path, args)


class RPCClient:
    def __init__(self, host="localhost", port=8080):
        """Initialize RPC client with host and port"""
        self.uri = f'ws://{host}:{port}'
        self.websocket = None
        self.request_id = 0
        
    async def connect(self):
        """Connect to the WebSocket server"""
        if not self.websocket:
            self.websocket = await websockets.connect(self.uri, subprotocols=['jsonrpc'])
            print(f"Connected to {self.uri}")
            
            # Get available methods
            components = await self.call_method("system.listComponents")
            print("Available methods:", components)
    
    async def close(self):
        """Close the WebSocket connection"""
        if self.websocket:
            await self.websocket.close()
            self.websocket = None
            
    async def call_method(self, method: str, params=None):
        """Make an RPC call to the server"""
        if not self.websocket:
            await self.connect()
            
        # Increment request ID
        self.request_id += 1
        
        # Prepare JSON-RPC request
        request = {
            'jsonrpc': '2.0',
            'method': method,
            'params': {'args': params} if params else [],
            'id': self.request_id
        }
        
        # Send request and wait for response
        print(f"Sending request: {json.dumps(request, indent=2)}")
        await self.websocket.send(json.dumps(request))
        response = await self.websocket.recv()
        print(f"Received response: {response}")
        
        # Parse and return result
        parsed = json.loads(response)
        if 'error' in parsed:
            raise Exception(f"RPC Error: {parsed['error']}")
        return parsed['result']
    
    def get_proxy(self, class_name: str) -> RPCProxy:
        """Get a proxy for a specific class"""
        return RPCProxy(self, class_name)


async def main():
    # Example usage
    client = RPCClient()
    try:
        # Get a proxy for the Calculator class
        calc = client.get_proxy("Calculator")
        
        # Make RPC calls using natural object-oriented syntax
        a, b = 5, 3
        result = await calc.add(a, b)
        print(f"add({a}, {b}) = {{'1': {result}}}")
        
        a, b = 10, 4
        result = await calc.subtract(a, b)
        print(f"subtract({a}, {b}) = {{'2': {result}}}")
        
        a, b = 6, 7
        result = await calc.multiply(a, b)
        print(f"multiply({a}, {b}) = {{'3': {result}}}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
