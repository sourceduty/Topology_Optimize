# Windows 11 Directory Topology Text
# Copyright (C) 2024, Sourceduty - All Rights Reserved.
# Write the directory topology of a given root directory on Windows 11 to a topology.txt file.

import os
import sys

def process_directory(current_dir, file_handle, indent_level, stats):
    """Recursively writes the directory structure to the file and updates stats."""
    try:
        items = os.listdir(current_dir)
    except PermissionError:
        # Skip directories that cannot be accessed
        stats['unreadable_dirs'] += 1
        return
    except FileNotFoundError:
        # Directory was removed during processing
        return

    items.sort()
    for item in items:
        itempath = os.path.join(current_dir, item)
        indent = '    ' * indent_level
        if os.path.isdir(itempath):
            file_handle.write(f"{indent}{item}/\n")
            stats['directories'] += 1
            process_directory(itempath, file_handle, indent_level + 1, stats)
        else:
            file_handle.write(f"{indent}{item}\n")
            stats['files'] += 1
            # Add file size to total size
            try:
                stats['total_size'] += os.path.getsize(itempath)
            except (OSError, PermissionError):
                # Skip files that cannot be accessed
                stats['unreadable_files'] += 1

def format_size(bytes_size):
    """Formats the size in bytes to a more readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} PB"

if __name__ == '__main__':
    # Always ask the user for the root directory
    root_dir = input("Enter the root directory: ")

    # Check if the provided root directory exists
    if not os.path.isdir(root_dir):
        print(f"The directory '{root_dir}' does not exist or is not a directory.")
        sys.exit(1)

    # Initialize statistics
    stats = {
        'directories': 1,  # Count the root directory
        'files': 0,
        'total_size': 0,
        'unreadable_dirs': 0,
        'unreadable_files': 0
    }

    # Open the topology.txt file for writing
    with open('topology.txt', 'w', encoding='utf-8') as f:
        f.write(f"{os.path.basename(root_dir)}/\n")
        process_directory(root_dir, f, 1, stats)

    # Prepare the statistics summary
    stats_summary = (
        f"Directory Topology Statistics:\n"
        f"Total Directories: {stats['directories']}\n"
        f"Total Files: {stats['files']}\n"
        f"Total Size: {format_size(stats['total_size'])}\n"
        f"Unreadable Directories: {stats['unreadable_dirs']}\n"
        f"Unreadable Files: {stats['unreadable_files']}\n\n"
    )

    # Read the existing topology content
    with open('topology.txt', 'r', encoding='utf-8') as f:
        topology_content = f.read()

    # Write the statistics summary at the top of the file
    with open('topology.txt', 'w', encoding='utf-8') as f:
        f.write(stats_summary + topology_content)

    print("Directory topology has been written to 'topology.txt'.")
