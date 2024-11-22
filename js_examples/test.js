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

        // console.log(this.getCall()("Calculator.add"));
        try {
            // Test calculator methods
            console.log('\nDEBUG: Testing Calculator methods...');

            await this.add(5, 3);
            await this.subtract(10, 4);
            await this.multiply(6, 7);

            console.log('DEBUG: All tests completed successfully');
        } catch (error) {
            console.error('DEBUG: Error in runTests:', error.message);
            console.error('DEBUG: Error stack:', error.stack);
            throw error;
        }
    }

    printMembers() {
        console.log('\nDEBUG: CalculatorClient members:');
        console.log('- Methods:', Object.getOwnPropertyNames(Object.getPrototypeOf(this)));
        console.log('- Instance variables:', Object.getOwnPropertyNames(this));
        console.log('- Complete instance:', this);
        
        // Print method details
        const proto = Object.getPrototypeOf(this);
        const methods = Object.getOwnPropertyNames(proto);
        console.log('\nDEBUG: Method details:');
        methods.forEach(method => {
            if (method !== 'constructor') {
                const descriptor = Object.getOwnPropertyDescriptor(proto, method);
                console.log(`- ${method}:`, descriptor);
            }
        });
    }
}

async function main() {
    let jrnc = null;
    console.log('DEBUG: Starting main...');
    try {
        // Create JRPC client with WebSocket URI
        console.log('DEBUG: Creating JRPCNodeClient...');
        jrnc = new JRPCNodeClient('ws://localhost:8080');
        console.log('DEBUG: JRPCNodeClient created');

        // Create and add calculator
        console.log('DEBUG: Creating CalculatorClient...');
        let cc = new CalculatorClient();
        console.log('DEBUG: Adding CalculatorClient to JRPCNodeClient...');
        jrnc.addClass(cc);
        console.log('DEBUG: CalculatorClient added');

        // Wait 1 second after addClass
        console.log('DEBUG: Waiting 1 second after addClass...');
        await new Promise(resolve => setTimeout(resolve, 500));

        // // Wait for remote to be up
        // console.log('\nDEBUG: Waiting for remote...');
        // await jrnc.remoteIsUp;
        // console.log('DEBUG: Remote is up');

        // Run all calculator tests
        cc.runTests();

        // Wait a bit before closing to ensure all messages are processed
        // await new Promise(resolve => setTimeout(resolve, 1000));
    } catch (error) {
        console.error('DEBUG: Error in main:', error.message);
        console.error('DEBUG: Error stack:', error.stack);
        process.exit(1);
    }
    
    // Keep running until Ctrl-C
    console.log('Running... Press Ctrl-C to exit');
    await new Promise(() => {}); // Never resolves, keeps process alive
}

// Handle process termination
process.on('SIGINT', () => {
    console.log('Received SIGINT. Exiting...');
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('Received SIGTERM. Exiting...');
    process.exit(0);
});

console.log('DEBUG: Script starting...');
main().catch(error => {
    console.error('Unhandled error:', error);
    process.exit(1);
});
console.log('DEBUG: Script started');
