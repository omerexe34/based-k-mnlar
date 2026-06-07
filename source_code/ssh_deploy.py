import paramiko

def run_ssh():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Connecting to VPS...")
        client.connect(
            hostname="89.47.113.37",
            username="root",
            password="StQCqZUfpyPp1_",
            timeout=10
        )
        print("Connected!")
        
        stdin, stdout, stderr = client.exec_command("uname -a; free -h; ls -la")
        print("STDOUT:")
        print(stdout.read().decode())
        print("STDERR:")
        print(stderr.read().decode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_ssh()
