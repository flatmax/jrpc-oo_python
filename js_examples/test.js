"use strict";

const JRPCNodeClient = require('jrpc-oo/JRPCNodeClient').JRPCNodeClient;

async function main() {
    try {
        // Create JRPC client with WebSocket URI
        const client = new JRPCNodeClient('ws://localhost:8080');
        
        // Now we can use the Calculator methods
        const result = await client.call['Calculator.add'](5, 3);
        console.log('5 + 3 =', result);
        
        // List available components
        console.log('\nAvailable components:');
        const components = await client.call['system.listComponents']();
        console.log(JSON.stringify(components, null, 2));
    } catch (error) {
        console.error('Error:', error.message);
    }
}

main();
