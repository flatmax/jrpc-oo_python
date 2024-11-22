"use strict";

const JRPCNodeClient = require('jrpc-oo/JRPCNodeClient').JRPCNodeClient;

class CalculatorClient {
    get call() { return this.getCall(); }

    async add(a, b) {
        console.log('\nDEBUG: Testing Calculator.add...');
        const result = await this.call["Calculator.add"](a, b);
        console.log('Full response:', JSON.stringify(result, null, 2));
        console.log(`${a} + ${b} = ${result.result}`);
        return result;
    }

    async subtract(a, b) {
        console.log('\nDEBUG: Testing Calculator.subtract...');
        const result = await this.call["Calculator.subtract"](a, b);
        console.log('Full response:', JSON.stringify(result, null, 2));
        console.log(`${a} - ${b} = ${result.result}`);
        return result;
    }

    async multiply(a, b) {
        console.log('\nDEBUG: Testing Calculator.multiply...');
        const result = await this.call["Calculator.multiply"](a, b);
        console.log('Full response:', JSON.stringify(result, null, 2));
        console.log(`${a} * ${b} = ${result.result}`);
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
    let jrpc = null;
    console.log('DEBUG: Starting main...');
    try {
        console.log('DEBUG: Creating JRPCNodeClient...');
        jrpc = new JRPCNodeClient('ws://localhost:8080');
        console.log('DEBUG: JRPCNodeClient created');
        
        console.log('DEBUG: Creating CalculatorClient...');
        let cc = new CalculatorClient();
        console.log('DEBUG: Adding CalculatorClient to JRPCNodeClient...');
        jrpc.addClass(cc);
        console.log('DEBUG: CalculatorClient added');
        
        // Wait for connection to establish
        await new Promise(resolve => setTimeout(resolve, 500));
        await cc.runTests();
        
        console.log('Running... Press Ctrl-C to exit');
        await new Promise(() => {});
        
    } catch (error) {
        console.error('Error:', error.message);
        process.exit(1);
    }
}

process.on('SIGINT', () => {
    console.log('Received SIGINT. Exiting...');
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('Received SIGTERM. Exiting...');
    process.exit(0);
});

main().catch(error => {
    console.error('Unhandled error:', error);
    process.exit(1);
});
