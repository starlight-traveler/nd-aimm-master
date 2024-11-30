import asyncio
import json
from datetime import datetime
from aiohttp import web, WSMsgType

# Maximum number of messages to store per port
MAX_MESSAGES_PER_PORT = 15  # Adjust as needed

# Store logs and connected websockets
logs = {port: [] for port in [9001, 9002, 9003, 9004, 9005, 9006]}
logs['critical'] = []  # Store critical messages
logs['buttons'] = []   # Store logs from button clicks
log_queues = {port: asyncio.Queue() for port in logs}
websockets = set()

# TCP client handler with port binding
async def handle_tcp_client(reader, writer, port):
    while True:
        data = await reader.readline()  # Assuming messages end with '\n'
        if not data:
            break
        try:
            message = data.decode('utf-8').strip()
            log_entry = json.loads(message)
            log_entry['port'] = port  # Add port information to log entry

            # Handle critical messages
            if log_entry.get('level') == 'CRITICAL':
                logs['critical'].append(log_entry)
                if len(logs['critical']) > MAX_MESSAGES_PER_PORT:
                    logs['critical'].pop(0)
                await log_queues['critical'].put(log_entry)

            # Store log entry per port
            logs[port].append(log_entry)
            if len(logs[port]) > MAX_MESSAGES_PER_PORT:
                logs[port].pop(0)
            await log_queues[port].put(log_entry)
        except Exception as e:
            print(f"Error processing log message: {e}")
    writer.close()
    await writer.wait_closed()

# Start TCP server on given host and port
async def start_tcp_server(host, port):
    async def client_connected(reader, writer):
        await handle_tcp_client(reader, writer, port)
    server = await asyncio.start_server(client_connected, host, port)
    print(f"Listening for logs on {host}:{port}")
    return server

# WebSocket handler for clients
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Send existing logs to the new client
    for port, port_logs in logs.items():
        for log in port_logs:
            await ws.send_json(log)

    websockets.add(ws)
    try:
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    # Handle messages from client
                    if data.get('action') == 'button_click':
                        button_id = data.get('buttonId')
                        # Execute the function mapped to the button
                        await execute_button_function(button_id)
                except Exception as e:
                    print(f"Error handling message from client: {e}")
            elif msg.type == WSMsgType.ERROR:
                print(f"WebSocket error: {ws.exception()}")
    finally:
        websockets.remove(ws)
    return ws

# Function to execute based on button click
async def execute_button_function(button_id):
    # Map each button to a specific function
    button_functions = {
        'button1': function_one,
        'button2': function_two,
        'button3': function_three,
        'button4': function_four,
        'button5': function_five,
        'button6': function_six,
    }
    func = button_functions.get(button_id)
    if func:
        await func()
    else:
        print(f"No function mapped to {button_id}")

# Define the functions to execute on button click
async def function_one():
    # Hardcoded function for button1
    print("Executing Function One")
    await log_event('Event One', 'INFO', 'Function One executed.')

async def function_two():
    print("Executing Function Two")
    await log_event('Event Two', 'INFO', 'Function Two executed.')

async def function_three():
    print("Executing Function Three")
    await log_event('Event Three', 'INFO', 'Function Three executed.')

async def function_four():
    print("Executing Function Four")
    await log_event('Event Four', 'INFO', 'Function Four executed.')

async def function_five():
    print("Executing Function Five")
    await log_event('Event Five', 'INFO', 'Function Five executed.')

async def function_six():
    print("Executing Function Six")
    await log_event('Event Six', 'INFO', 'Function Six executed.')

# Function to log events and notify clients
async def log_event(event_name, level, message):
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'logger': 'ButtonFunctionLogger',
        'level': level,
        'message': message,
        'port': 'buttons'
    }

    # Store the log entry
    logs['buttons'].append(log_entry)
    if len(logs['buttons']) > MAX_MESSAGES_PER_PORT:
        logs['buttons'].pop(0)

    # Put the log entry in the queue
    await log_queues['buttons'].put(log_entry)

# Notify all connected clients about a new log entry
async def notify_clients(port):
    while True:
        log_entry = await log_queues[port].get()
        for ws in websockets:
            await ws.send_json(log_entry)

# Serve the index.html file
async def index(request):
    with open('index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return web.Response(text=html_content, content_type='text/html')

# Main function to start servers and tasks
async def main():
    # Start TCP servers on multiple ports
    ports = [9001, 9002, 9003, 9004, 9005, 9006]
    servers = [await start_tcp_server('0.0.0.0', port) for port in ports]

    # Start background tasks to notify clients
    for port in ports + ['critical', 'buttons']:
        asyncio.create_task(notify_clients(port))

    # Set up web application
    app = web.Application()
    app.add_routes([web.get('/', index)])
    app.add_routes([web.get('/ws', websocket_handler)])
    app.router.add_static('/static/', path='static', name='static')  # For CSS files if needed

    # Start web server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()

    print("Web interface available at http://0.0.0.0:8080")

    # Keep the program running
    await asyncio.Event().wait()

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
