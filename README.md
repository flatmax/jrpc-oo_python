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
from src.client import RPCClient

async def main():
    # Create client
    client = RPCClient('ws://localhost:8080')
    await client.connect()
    
    # Use Calculator methods
    result = await client.call_method("Calculator.add", [5, 3])
    print('5 + 3 =', result)

if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript Client Example

```javascript
const JRPCNodeClient = require('jrpc-oo/JRPCNodeClient').JRPCNodeClient;

class CalculatorClient {
    get call() { return this.getCall(); }

    async add(a, b) {
        const result = await this.call["Calculator.add"](a, b);
        console.log(`${a} + ${b} = ${result.result}`);
        return result;
    }

    async subtract(a, b) {
        const result = await this.call["Calculator.subtract"](a, b);
        console.log(`${a} - ${b} = ${result.result}`);
        return result;
    }

    async multiply(a, b) {
        const result = await this.call["Calculator.multiply"](a, b);
        console.log(`${a} * ${b} = ${result.result}`);
        return result;
    }

    // Optional: method to run all operations
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
        
        // Run individual operations
        await calc.add(5, 3);
        await calc.subtract(10, 4);
        
        // Or run all operations at once
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
│   ├── server.py
│   └── client.py
└── js_examples/
    ├── package.json
    └── test.js
```

### Running Tests

```bash
# Start the server
python src/server.py

# In another terminal, run JavaScript example
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
