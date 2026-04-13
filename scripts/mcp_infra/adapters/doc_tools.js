#!/usr/bin/env node
const { spawn } = require('child_process');

// Word Document Tools MCP often outputs non-JSON noise at startup.
// This adapter ensures ONLY JSON messages are passed to the parent (STDOUT).

const child = spawn('npx', ['-y', '--quiet', '@puchunjie/doc-tools-mcp'], {
    stdio: ['pipe', 'pipe', 'inherit'],
    shell: true
});

let foundStart = false;

child.stdout.on('data', (data) => {
    if (foundStart) {
        process.stdout.write(data);
    } else {
        const str = data.toString();
        const firstBrace = str.indexOf('{');
        if (firstBrace !== -1) {
            process.stdout.write(str.substring(firstBrace));
            foundStart = true;
        }
    }
});

child.on('close', (code) => {
    process.exit(code);
});

child.on('error', (err) => {
    console.error('Failed to start child process:', err);
    process.exit(1);
});

process.stdin.pipe(child.stdin);
