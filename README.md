# NDAIMM Live Logs Viewer

Welcome to the **NDAIMM Live Logs Viewer**, a real-time logging dashboard designed to monitor logs from multiple computers in your network. This system captures log messages sent over TCP and displays them in a user-friendly web interface with dynamic status lights and filtering capabilities.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Ports and Computer Assignments](#ports-and-computer-assignments)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Triggering Status Lights](#triggering-status-lights)
- [Using the Live Logs Viewer](#using-the-live-logs-viewer)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The NDAIMM Live Logs Viewer is built using Python's `asyncio` and `aiohttp` libraries to handle multiple TCP connections and WebSocket clients efficiently. Logs are categorized by their source ports and displayed with visual indicators (status lights) to highlight important events.

## Features

- **Real-Time Log Monitoring:** View logs from multiple computers in real-time.
- **Dynamic Status Lights:** Visual indicators that activate based on specific log messages or levels.
- **Filtering:** Easily filter logs by severity levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
- **Responsive Design:** Accessible from various devices with a clean and modern interface.
- **Critical Messages Box:** A dedicated section for high-severity (`CRITICAL`) logs from all sources.

## Ports and Computer Assignments

Logs are collected from different computers, each assigned to a specific TCP port:

```
Main Computer - 9001
Auxiliary Computer - 9002
Startup and Emergency Computer - 9003
Drone Computer - 9004
```

**Note:** Ensure that each computer is configured to send logs to its designated port.

## Installation

### Prerequisites

- **Python 3.7+** installed on your system.
- **Pip** package manager.

### Clone the Repository

```bash
git clone https://github.com/yourusername/ndaimm-live-logs-viewer.git
cd ndaimm-live-logs-viewer
```

### Install Dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**`requirements.txt`** should include:

```plaintext
aiohttp
PyYAML
```

*(Ensure to create or update the `requirements.txt` accordingly.)*

## Configuration

### `config.yaml`

The application uses a YAML configuration file to set up logging parameters and TCP logging settings.

```yaml
logging:
  version: 1
  disable_existing_loggers: False
  formatters:
    standard:
      format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
      datefmt: '%Y-%m-%d %H:%M:%S'
  handlers:
    console:
      class: logging.StreamHandler
      level: DEBUG
      formatter: standard
      stream: ext://sys.stdout
    file:
      class: logging.FileHandler
      level: DEBUG
      formatter: standard
      filename: 'logs/application.log'
  loggers:
    AuxiliaryLogger:
      level: DEBUG
      handlers: [console, file]
      propagate: False

tcp_logging:
  host: "127.0.0.1"   # Replace with server's IP address if different
  port: 9001          # Must match the assigned port for each computer
```

**Important:**

- **Multiple Configurations:** Each computer should have its own `config.yaml` with the corresponding `tcp_logging.port` value (e.g., 9001 for Main Computer, 9002 for Auxiliary Computer, etc.).
- **Log Directory:** Ensure that the log directory specified in `logging.handlers.file.filename` exists or is created by the application.

## Running the Application

### Start the Live Logs Viewer Server

```bash
python master_control.py
```

- **Server Listening Ports:** The server listens on the assigned ports (9001-9006) for incoming log messages.
- **Web Interface:** Accessible at [http://localhost:8080](http://localhost:8080).

### Sending Logs from Computers

Ensure each computer is configured to send logs to its designated TCP port as specified in the `config.yaml`. Logs should be sent as JSON strings terminated with a newline (`\n`).

**Example Log Entry:**

```json
{
  "timestamp": "2024-04-05T14:25:35.123456",
  "logger": "AuxiliaryLogger",
  "level": "INFO",
  "message": "System initialized successfully."
}
```

## Triggering Status Lights

The live logs viewer includes status lights that activate based on specific log messages or severity levels. Here's how you can trigger them:

### Status Lights Configuration

In the `index.html`, the `statusLightConfig` object defines how each light is triggered and its color.

```javascript
const statusLightConfig = {
    0: {
        trigger: (logEntry) => logEntry.message.toLowerCase().includes('error'),
        color: '#ff1744'  // Red
    },
    1: {
        trigger: (logEntry) => logEntry.message.toLowerCase().includes('warning'),
        color: '#ffea00'  // Yellow
    },
    2: {
        trigger: (logEntry) => logEntry.message.toLowerCase().includes('connected'),
        color: '#00e676'  // Green
    },
    3: {
        trigger: (logEntry) => logEntry.message.toLowerCase().includes('disconnected'),
        color: '#ff6d00'  // Orange
    },
    4: {
        trigger: (logEntry) => logEntry.level === 'CRITICAL',
        color: '#d500f9'  // Purple
    },
    5: {
        trigger: (logEntry) => logEntry.message.toLowerCase().includes('processing'),
        color: '#2979ff'  // Blue
    },
    6: {
        trigger: (logEntry) => logEntry.message.toLowerCase().includes('uploaded'),
        color: '#00bfa5'  // Teal
    },
    7: {
        trigger: (logEntry) => logEntry.message.toLowerCase().includes('executed'),
        color: '#651fff'  // Deep Purple
    },
};
```

### How to Trigger Each Light

1. **Light 0 - Red (`#ff1744`):**
   - **Trigger:** Any log message containing the keyword `error`.
   - **Example Message:** `"An error occurred while processing the request."`

2. **Light 1 - Yellow (`#ffea00`):**
   - **Trigger:** Any log message containing the keyword `warning`.
   - **Example Message:** `"Warning: Disk space running low."`

3. **Light 2 - Green (`#00e676`):**
   - **Trigger:** Any log message containing the keyword `connected`.
   - **Example Message:** `"Client connected successfully."`

4. **Light 3 - Orange (`#ff6d00`):**
   - **Trigger:** Any log message containing the keyword `disconnected`.
   - **Example Message:** `"Client disconnected unexpectedly."`

5. **Light 4 - Purple (`#d500f9`):**
   - **Trigger:** Any log message with the severity level `CRITICAL`.
   - **Example Message:** `"CRITICAL: System failure detected."`

6. **Light 5 - Blue (`#2979ff`):**
   - **Trigger:** Any log message containing the keyword `processing`.
   - **Example Message:** `"Processing data batch 42."`

7. **Light 6 - Teal (`#00bfa5`):**
   - **Trigger:** Any log message containing the keyword `uploaded`.
   - **Example Message:** `"File uploaded successfully."`

8. **Light 7 - Deep Purple (`#651fff`):**
   - **Trigger:** Any log message containing the keyword `executed`.
   - **Example Message:** `"Executed scheduled task."`

### Customizing Status Lights

To customize the triggers or colors:

1. **Edit the `statusLightConfig` in `index.html`:**

```javascript
const statusLightConfig = {
    // Existing configurations...
    0: {
        trigger: (logEntry) => logEntry.message.toLowerCase().includes('error'),
        color: '#ff1744'  // Red
    },
    // Add or modify configurations as needed
};
```

2. **Define New Triggers or Change Colors:**

   - **Add a New Light:**

     ```javascript
     8: {
         trigger: (logEntry) => logEntry.message.toLowerCase().includes('maintenance'),
         color: '#ffa726'  // Orange
     },
     ```

   - **Change an Existing Light's Color:**

     ```javascript
     0: {
         trigger: (logEntry) => logEntry.message.toLowerCase().includes('error'),
         color: '#e53935'  // Changed Red shade
     },
     ```

3. **Update the Status Lights in HTML:**

   - If adding more lights beyond the initial 8, ensure the HTML reflects the new number.

## Using the Live Logs Viewer

### Accessing the Dashboard

Open your web browser and navigate to:

```
http://localhost:8080
```

### Interface Overview

- **Header:** Displays the application name "NDAIMM".
- **Log Boxes:** Each box corresponds to a computer and displays its logs.
  - **Box Header:**
    - **Title:** Name of the computer (e.g., "Main Computer").
    - **Filter Dropdown:** Allows filtering logs by severity level.
    - **Status Lights:** Visual indicators that activate based on log content or level.
- **Log Area:** Displays log entries with timestamps, levels, and messages.

### Filtering Logs

1. **Select a Level:** Use the dropdown menu in the box header to select the desired log level (`ALL`, `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
2. **View Filtered Logs:** Only logs matching the selected level will be displayed.
3. **Switching Filters:** Changing the filter does not erase existing logs; it merely shows or hides logs based on the selected criteria.

### Critical Messages Box

A dedicated box at the top displays all `CRITICAL` logs from all computers, ensuring that high-severity events are prominently visible.

## Customization

### Changing Log Display Limits

- **Maximum Messages per Box:**
  - Located in the JavaScript section of `index.html`:
  
    ```javascript
    const MAX_MESSAGES_PER_BOX = 15; // Adjust as needed
    ```
  
  - Modify this value to increase or decrease the number of visible logs per box.

- **Total Stored Messages:**
  - To prevent unbounded memory usage, the application stores a limited number of messages in memory (e.g., 100).
  - Adjust this in the `addLogEntryToBox` function:

    ```javascript
    if (messages.length > 100) { // Adjust as needed
        messages.shift();
    }
    ```

### Styling Adjustments

- **Colors and Fonts:**
  - Modify the CSS in the `<style>` section to change colors, fonts, or layout as desired.

- **Responsive Design:**
  - Ensure that any changes maintain the responsiveness of the interface across different devices.

## Troubleshooting

### Logs Not Appearing in the Dashboard

1. **Check Server Status:**
   - Ensure `master_control.py` is running without errors.
   - Verify that the server is listening on the correct ports (9001-9006).

2. **Verify Log Sending:**
   - Ensure that each computer is configured to send logs to its assigned port.
   - Use tools like `telnet` or `nc` to test TCP connections.

3. **Inspect WebSocket Connection:**
   - Open browser developer tools (F12) and check the Network tab for WebSocket connections.
   - Ensure that the WebSocket connection to `/ws` is established successfully.

4. **Review Console Outputs:**
   - Check both server and client console outputs for any error messages or connection issues.

5. **Firewall and Network Settings:**
   - Ensure that firewalls are not blocking the designated ports.
   - Verify network configurations if accessing the dashboard remotely.

### Status Lights Not Activating

1. **Ensure Correct Triggers:**
   - Verify that log messages contain the keywords or levels defined in `statusLightConfig`.

2. **Check Light Configuration:**
   - Confirm that `statusLightConfig` is correctly defined in `index.html`.

3. **Inspect JavaScript Errors:**
   - Use browser developer tools to check for any JavaScript errors that might prevent status lights from functioning.

4. **Validate Log Message Format:**
   - Ensure that log messages include the necessary fields (`level`, `message`, etc.) as expected by the dashboard.

## License

This project is licensed under the [MIT License](LICENSE).

---

**Feel free to contribute, suggest improvements, or report issues by opening an [issue](https://github.com/yourusername/ndaimm-live-logs-viewer/issues) on GitHub.**

```html
// Configuration for status lights
        const statusLightConfig = {
            0: {
                trigger: (logEntry) => logEntry.message.toLowerCase().includes('error'),
                color: '#ff1744'  // Red
            },
            1: {
                trigger: (logEntry) => logEntry.message.toLowerCase().includes('warning'),
                color: '#ffea00'  // Yellow
            },
            2: {
                trigger: (logEntry) => logEntry.message.toLowerCase().includes('connected'),
                color: '#00e676'  // Green
            },
            3: {
                trigger: (logEntry) => logEntry.message.toLowerCase().includes('disconnected'),
                color: '#ff6d00'  // Orange
            },
            4: {
                trigger: (logEntry) => logEntry.level === 'CRITICAL',
                color: '#d500f9'  // Purple
            },
            5: {
                trigger: (logEntry) => logEntry.message.toLowerCase().includes('processing'),
                color: '#2979ff'  // Blue
            },
            6: {
                trigger: (logEntry) => logEntry.message.toLowerCase().includes('uploaded'),
                color: '#00bfa5'  // Teal
            },
            7: {
                trigger: (logEntry) => logEntry.message.toLowerCase().includes('executed'),
                color: '#651fff'  // Deep Purple
            },
        };

        // Configuration for big lights
        const bigLightConfig = {
            0: {
                trigger: (logEntry) => logEntry.message.toLowerCase().includes('event one'),
                color: '#ff1744'  // Red
            },
            1: {
                trigger: (logEntry) => logEntry.message.toLowerCase().includes('event two'),
                color: '#ffea00'  // Yellow
            },
            2: {
                trigger: (logEntry) => logEntry.message.toLowerCase().includes('event three'),
                color: '#00e676'  // Green
            },
            3: {
                trigger: (logEntry) => logEntry.message.toLowerCase().includes('event four'),
                color: '#2979ff'  // Blue
            },
            4: {
                trigger: (logEntry) => logEntry.message.toLowerCase().includes('event five'),
                color: '#d500f9'  // Purple
            },
            5: {
                trigger: (logEntry) => logEntry.message.toLowerCase().includes('event six'),
                color: '#ff6d00'  // Orange
            }
        };
```