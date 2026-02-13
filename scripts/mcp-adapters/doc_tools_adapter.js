/**
 * MCP Adapter for @puchunjie/doc-tools-mcp
 * Solves the "invalid character 'W'" error by filtering out the
 * non-JSON startup message: "Word Document Tools MCP 服务器已启动"
 */
const { spawn } = require('child_process');

const child = spawn('npx', ['-y', '--quiet', '@puchunjie/doc-tools-mcp'], {
    shell: true,
    stdio: ['pipe', 'pipe', 'inherit']
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

child.on('exit', (code) => {
    process.exit(code);
});

process.stdin.pipe(child.stdin);
