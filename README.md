# jrpc-oo_python

A Python implementation of the jrpc-oo protocol, enabling seamless communication between Python and JavaScript using an object-oriented approach.

## Features

- JSON-RPC 2.0 compliant
- WebSocket-based communication
- Class-based RPC approach
- Dynamic method discovery
- Cross-language compatibility focus
- Automatic method discovery via `system.listComponents`
- Debug logging support
- Comprehensive error handling

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

```bash
python src/server.py
```

The server will display all registered classes and methods on startup.

### Python Client Example

```python
from src.jrpc_client import JRPCClient
import asyncio

async def main():
    # Create client
    client = JRPCClient('localhost', 8080)
    
    try:
        # Access Calculator methods using dictionary style
        calc = client['Calculator']
        
        # Use Calculator methods
        result = await calc.add(5, 3)
        print('5 + 3 =', result)
        
        result = await calc.multiply(6, 7)
        print('6 * 7 =', result)
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

### Server Example

```python
from src.jrpc_server import JRPCServer
import asyncio

class Calculator:
    def add(self, a, b):
        return a + b
    
    def multiply(self, a, b):
        return a * b

if __name__ == "__main__":
    # Create and configure server
    server = JRPCServer(host='localhost', port=8080)
    
    # Register calculator instance
    server.register_instance(Calculator())
    
    # Start server
    asyncio.get_event_loop().run_until_complete(server.start())
    asyncio.get_event_loop().run_forever()
```

### JavaScript Client Example

```javascript
const JRPCNodeClient = require('jrpc-oo/JRPCNodeClient').JRPCNodeClient;

class CalculatorClient {
    get call() { return this.getCall(); }

    async add(a, b) {
        console.log('\nDEBUG: Testing Calculator.add...');
        const result = await this.call["Calculator.add"](a, b);
        const value = Object.values(result)[0];  // Get the first (and only) value
        console.log(`${a} + ${b} = ${value}`);
        return result;
    }

    async subtract(a, b) {
        console.log('\nDEBUG: Testing Calculator.subtract...');
        const result = await this.call["Calculator.subtract"](a, b);
        const value = Object.values(result)[0];
        console.log(`${a} - ${b} = ${value}`);
        return result;
    }

    async multiply(a, b) {
        console.log('\nDEBUG: Testing Calculator.multiply...');
        const result = await this.call["Calculator.multiply"](a, b);
        const value = Object.values(result)[0];
        console.log(`${a} * ${b} = ${value}`);
        return result;
    }

    async runTests() {
        try {
            await this.add(5, 3);
            await this.subtract(10, 4);
            await this.multiply(6, 7);
        } catch (error) {
            console.error('Error:', error.message);
            throw error;
        }
    }
}

async function main() {
    try {
        // Create and setup RPC client
        const jrpc = new JRPCNodeClient('ws://localhost:8080');
        const calc = new CalculatorClient();
        jrpc.addClass(calc);
        
        // Wait for connection to establish
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Run all operations
        await calc.runTests();
        
        // Keep the connection alive
        console.log('Running... Press Ctrl-C to exit');
        await new Promise(() => {});
        
    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    }
}

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log('Received SIGINT. Exiting...');
    process.exit(0);
});

main().catch(error => {
    console.error('Unhandled error:', error);
    process.exit(1);
});
```

## Protocol Support

### WebSocket
- URL format: `ws://hostname:port`
- Uses `websockets` library for Python server
- Full-duplex communication
- Ideal for real-time applications

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
jrpc-oo_python/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── server.py        # Example server with Calculator class
│   ├── jrpc_server.py   # Core RPC server implementation
│   ├── client.py        # Example client usage
│   └── jrpc_client.py   # Core RPC client implementation
└── js_examples/
    ├── package.json
    └── test.js          # JavaScript client example
```

### Running Tests

```bash
# Start the server
python src/server.py

# In another terminal, run the Python client
python src/client.py

# Or run the JavaScript client
cd js_examples
node test.js
```

## Contributing

1. Fork it
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
