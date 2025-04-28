# Ping-Starter

A utility that executes batch files based on network connectivity status.

## Overview

Ping-Starter monitors a specified IP address by pinging it at regular intervals. Based on the connectivity status, it executes batch files from designated folders:

-   When a device becomes reachable (after being unreachable), it executes all `.bat` files in the `reachable` folder.
-   When a device becomes unreachable (after being reachable), it executes all `.bat` files in the `not_reachable` folder.

The application only executes batch files when there's a state change, preventing repeated executions while in the same state.

## Setup

1. Ensure Python 3.6+ is installed on your system
2. Clone or download this repository
3. Configure the `settings.ini` file with your desired parameters
4. Place your batch files in the appropriate folders:
    - `reachable/` - Batch files to execute when the device becomes reachable
    - `not_reachable/` - Batch files to execute when the device becomes unreachable
5. Run the application with `python main.py`

## Configuration

The application uses a `settings.ini` file with the following parameters:

```ini
[Settings]
ip_address = 192.168.1.1    # The IP address to monitor
ping_interval = 10          # Time between pings in seconds
ping_limit = 3              # Number of consecutive successful/failed pings required to trigger a state change
```

### Parameters Explained

-   **ip_address**: The IP address of the device you want to monitor
-   **ping_interval**: How often (in seconds) the application should ping the device
-   **ping_limit**: How many consecutive successful or failed pings are required before executing batch files

## How It Works

1. The application reads the configuration from `settings.ini`
2. It enters a continuous loop:
    - Pings the specified IP address
    - Tracks consecutive successful and failed pings
    - When the number of consecutive successful pings reaches the limit, and the previous state was "unreachable" or unknown:
        - Changes the state to "reachable"
        - Executes all `.bat` files in the `reachable/` folder
    - When the number of consecutive failed pings reaches the limit, and the previous state was "reachable" or unknown:
        - Changes the state to "unreachable"
        - Executes all `.bat` files in the `not_reachable/` folder
    - Waits for the specified interval before pinging again

## Use Cases

-   **Home Automation**: Execute scripts when your mobile device connects to or disconnects from your home network
-   **Network Monitoring**: Trigger alerts or recovery procedures when critical network devices go offline
-   **Remote Management**: Start or stop services based on the availability of a remote server
-   **Power Management**: Turn on/off devices when a specific network device becomes available or unavailable

## Terminating the Application

To stop the application, press `Ctrl+C` in the terminal where it's running.

## License

See the [LICENSE](LICENSE) file for details.
