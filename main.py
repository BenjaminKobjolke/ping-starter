#!/usr/bin/env python3
"""
Ping Starter - A utility to execute batch files based on network connectivity.

This script monitors a specified IP address and executes batch files in the
appropriate folder based on whether the IP is reachable or not.
"""

import configparser
import os
import subprocess
import time
from ping3 import ping
from datetime import datetime

def read_settings():
    """Read settings from the settings.ini file."""
    config = configparser.ConfigParser()
    config.read('settings.ini')
    
    settings = {
        'ip_address': config['Settings']['ip_address'],
        'ping_interval': int(config['Settings']['ping_interval']),
        'ping_limit': int(config['Settings']['ping_limit'])
    }
    
    return settings

def ping_host(host, timeout=1):
    """
    Ping the specified host and return True if reachable, False otherwise.
    Uses ping3 library for cross-platform compatibility.
    """
    try:
        response_time = ping(host, timeout=timeout)
        # ping() returns None or False on failure, and the response time (float) on success
        return response_time is not None and response_time != False
    except Exception as e:
        print(f"Error pinging {host}: {e}")
        return False

def execute_batch_files(folder):
    """Execute all .bat files in the specified folder."""
    print(f"Executing batch files in {folder} folder...")
    
    # Ensure the folder exists
    if not os.path.exists(folder):
        print(f"Folder {folder} does not exist.")
        return
    
    # Get all .bat files in the folder
    bat_files = [f for f in os.listdir(folder) if f.endswith('.bat')]
    
    if not bat_files:
        print(f"No .bat files found in {folder}.")
        return
    
    # Execute each .bat file
    for bat_file in bat_files:
        bat_path = os.path.join(folder, bat_file)
        print(f"Executing {bat_path}...")
        try:
            subprocess.run([bat_path], check=True)
            print(f"Successfully executed {bat_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing {bat_path}: {e}")
        except Exception as e:
            print(f"Unexpected error executing {bat_path}: {e}")

def main():
    """Main function to monitor IP and execute batch files."""
    settings = read_settings()
    ip_address = settings['ip_address']
    ping_interval = settings['ping_interval']
    ping_limit = settings['ping_limit']
    
    print(f"Starting Ping Starter")
    print(f"Monitoring IP: {ip_address}")
    print(f"Ping interval: {ping_interval} seconds")
    print(f"Ping limit: {ping_limit} consecutive pings")
    
    # Initialize state variables
    current_state = None  # None = unknown, True = reachable, False = not reachable
    consecutive_success = 0
    consecutive_failure = 0
    
    while True:
        # Get current time for logging
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Ping the IP address
        is_reachable = ping_host(ip_address)
        
        if is_reachable:
            consecutive_success += 1
            consecutive_failure = 0
            print(f"[{current_time}] Ping successful. Consecutive successes: {consecutive_success}/{ping_limit}")
        else:
            consecutive_failure += 1
            consecutive_success = 0
            print(f"[{current_time}] Ping failed. Consecutive failures: {consecutive_failure}/{ping_limit}")
        
        # Check if state should change to reachable
        if consecutive_success >= ping_limit and current_state != True:
            print(f"[{current_time}] State changed to REACHABLE")
            current_state = True
            execute_batch_files('reachable')
        
        # Check if state should change to not reachable
        if consecutive_failure >= ping_limit and current_state != False:
            print(f"[{current_time}] State changed to NOT REACHABLE")
            current_state = False
            execute_batch_files('not_reachable')
        
        # Wait for the specified interval
        time.sleep(ping_interval)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPing Starter terminated by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
