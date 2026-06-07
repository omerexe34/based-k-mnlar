import paramiko

def check_logs():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect("89.47.113.37", username="root", password="StQCqZUfpyPp1_", timeout=10)
        
        # Check service status and recent logs
        stdin, stdout, stderr = client.exec_command("systemctl status freerider --no-pager")
        print("--- SERVICE STATUS ---")
        print(stdout.read().decode('utf-8', errors='replace'))
        
        stdin, stdout, stderr = client.exec_command("journalctl -u freerider -n 50 --no-pager")
        print("\n--- RECENT LOGS ---")
        print(stdout.read().decode('utf-8', errors='replace'))
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    check_logs()
