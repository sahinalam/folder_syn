# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 18:28:06 2024

@author: sahin
"""
import os
import shutil
import time
import argparse
from datetime import datetime

def log_message(message, log_file):
    """Log a message to the console and a log file."""
    print(message)
    with open(log_file, 'a') as f:
        f.write(f"{datetime.now()}: {message}\n")

def sync_folders(source, replica, log_file):
    """Synchronize the replica folder to match the source folder."""
    # Ensure replica directory exists
    if not os.path.exists(replica):
        os.makedirs(replica)
        log_message(f"Created directory: {replica}", log_file)

    # Get all files and directories in the source folder
    for root, dirs, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        target_root = os.path.join(replica, relative_path)

        # Create missing directories in the replica
        for directory in dirs:
            target_dir = os.path.join(target_root, directory)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
                log_message(f"Created directory: {target_dir}", log_file)

        # Copy files from source to replica
        for file in files:
            source_file = os.path.join(root, file)
            replica_file = os.path.join(target_root, file)
            if not os.path.exists(replica_file) or os.path.getmtime(source_file) != os.path.getmtime(replica_file):
                shutil.copy2(source_file, replica_file)
                log_message(f"Copied file: {source_file} to {replica_file}", log_file)

    # Remove files and directories from replica that are not in source
    for root, dirs, files in os.walk(replica, topdown=False):
        relative_path = os.path.relpath(root, replica)
        source_root = os.path.join(source, relative_path)

        # Remove files in the replica that are not in the source
        for file in files:
            replica_file = os.path.join(root, file)
            source_file = os.path.join(source_root, file)
            if not os.path.exists(source_file):
                os.remove(replica_file)
                log_message(f"Removed file: {replica_file}", log_file)

        # Remove directories in the replica that are not in the source
        for directory in dirs:
            replica_dir = os.path.join(root, directory)
            source_dir = os.path.join(source_root, directory)
            if not os.path.exists(source_dir):
                shutil.rmtree(replica_dir)
                log_message(f"Removed directory: {replica_dir}", log_file)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Synchronize two folders.")
    parser.add_argument('--source', required=True, help='Path to the source folder')
    parser.add_argument('--interval', type=int, required=True, help='Synchronization interval in seconds')
    parser.add_argument('--log', required=True, help='Path to the log file')
    args = parser.parse_args()

    # Set the default replica directory under the current working directory
    replica = os.path.join(os.getcwd(), 'replica')

    # Run synchronization periodically
    while True:
        try:
            sync_folders(args.source, replica, args.log)
        except Exception as e:
            log_message(f"Error during synchronization: {str(e)}", args.log)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
