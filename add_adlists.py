import sqlite3
import sys
import os

# Check if running as root
if os.geteuid() != 0:
    print("This script must be run as root (sudo).")
    sys.exit(1)

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <path_to_domains_file>")
    sys.exit(1)

file_path = sys.argv[1]
db_path = '/etc/pihole/gravity.db'

if not os.path.exists(file_path):
    print(f"Error: File '{file_path}' not found.")
    sys.exit(1)

print(f"Reading adlists from {file_path}...")

try:
    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)

print(f"Found {len(urls)} URLs.")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    added_count = 0
    for url in urls:
        # Check if already exists
        cursor.execute("SELECT id FROM adlist WHERE address = ?", (url,))
        if cursor.fetchone():
            print(f"Skipping (already exists): {url}")
        else:
            cursor.execute("INSERT INTO adlist (address, comment) VALUES (?, ?)", (url, "Added via script"))
            added_count += 1
            print(f"Added: {url}")
    
    conn.commit()
    conn.close()
    print(f"Successfully added {added_count} new adlists.")
    
    if added_count > 0:
        print("Updating Gravity...")
        os.system("pihole -g")
    else:
        print("No new adlists added. Gravity update skipped.")

except Exception as e:
    print(f"Database error: {e}")
    sys.exit(1)
