# JRPC2-PY-JS

A flexible JSON-RPC 2.0 implementation enabling seamless communication between Python and JavaScript using an object-oriented approach.

## Features

- JSON-RPC 2.0 compliant
- Class-based RPC approach
- Supports both HTTP and WebSocket protocols
- Method introspection support
- Dynamic proxy-based method calling
- Cross-language compatibility focus
- Automatic method discovery via `system.listComponents`

## Installation

### Python Dependencies

```bash
pip install -r requirements.txt
```

### JavaScript Dependencies

```bash
cd js_examples
npm install
```

## Usage

### Starting the Server

The server supports both HTTP and WebSocket protocols:

```bash
# HTTP Server (default)
python src/server.py

# WebSocket Server
python src/server.py ws
```

### Python Client Example

```python
from src.client import RPCClient

# Create client
client = RPCClient('http://localhost:8080')  # or 'ws://localhost:8080' for WebSocket

# Use Calculator methods
result = client.Calculator.add(5, 3)
print('5 + 3 =', result)
```

### JavaScript Client Example

```javascript
const JRPCNodeClient = require('jrpc-oo/JRPCNodeClient').JRPCNodeClient;

async function main() {
    // Create client
    const client = new JRPCNodeClient('ws://localhost:8080');
    
    // Use Calculator methods
    const result = await client.call['Calculator.add'](5, 3);
    console.log('5 + 3 =', result);
}
```

## Protocol Support

### HTTP (Default)
- URL format: `http://hostname:port`
- Uses `jsonrpclib-pelix` for Python server
- Standard HTTP JSON-RPC 2.0 protocol

### WebSocket
- URL format: `ws://hostname:port`
- Uses `websockets` library for Python server
- Full-duplex communication
- Better for real-time applications

## Available Components

### Calculator
A simple calculator class demonstrating RPC functionality:
- `add(a: float, b: float) -> float`: Add two numbers
- `subtract(a: float, b: float) -> float`: Subtract b from a
- `multiply(a: float, b: float) -> float`: Multiply two numbers

### System Methods
- `system.listComponents()`: Returns information about all registered classes and their methods

## Development

### Project Structure
```
jrpc2-py-js/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── server.py
│   └── client.py
├── js_examples/
│   ├── package.json
│   └── test.js
└── tests/
    ├── __init__.py
    └── test_rpc.py
```

### Running Tests

```bash
# Python tests
pytest tests/

# JavaScript example
cd js_examples
node test.js
```

## Security Considerations

- The server currently accepts all connections
- No built-in authentication mechanism
- Consider running behind a reverse proxy for production use
- Implement your own authentication layer if needed

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
