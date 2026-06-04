import paramiko

def run_ssh():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Connecting to VPS...")
        client.connect("89.47.113.37", username="root", password="StQCqZUfpyPp1_", timeout=10)
        
        setup_script = """
        apt-get update
        apt-get install -y docker-compose-plugin
        
        cd /root/supabase/docker
        
        echo "Pulling docker images (this might take a few minutes)..."
        docker compose pull
        echo "Starting Supabase..."
        docker compose up -d
        
        echo "Supabase setup done!"
        docker ps
        """
        
        print("Running Supabase installation...")
        stdin, stdout, stderr = client.exec_command(setup_script)
        
        for line in iter(stdout.readline, ""):
            print(line, end="")
            
        print("STDERR:")
        for line in iter(stderr.readline, ""):
            print(line, end="")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_ssh()
