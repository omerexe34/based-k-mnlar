import paramiko
import time

def run_ssh():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Connecting to VPS...")
        client.connect("89.47.113.37", username="root", password="StQCqZUfpyPp1_", timeout=10)
        
        print("Installing Cloudflare WARP and proxychains...")
        setup_cmds = [
            "apt-get update",
            "apt-get install -y curl gpg proxychains4 postgresql-client",
            "curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg",
            "echo 'deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ noble main' | tee /etc/apt/sources.list.d/cloudflare-client.list",
            "apt-get update",
            "apt-get install -y cloudflare-warp",
            "warp-cli --accept-tos registration new",
            "warp-cli --accept-tos mode proxy",
            "warp-cli --accept-tos connect",
            "sleep 5"
        ]
        
        for cmd in setup_cmds:
            print(f"Running: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            stdout.channel.recv_exit_status()
            
        print("Checking WARP status...")
        stdin, stdout, stderr = client.exec_command("warp-cli --accept-tos status")
        print(stdout.read().decode())
        
        # Configure proxychains
        print("Configuring proxychains...")
        client.exec_command("sed -i 's/^socks4 .*/socks5  127.0.0.1 40000/' /etc/proxychains4.conf").stdout.channel.recv_exit_status()
        
        # Run pg_dump via proxychains
        print("Running pg_dump via proxychains...")
        db_uri = "postgresql://postgres:jytrfvbnjuytrfvbn@db.xrzepgacyugeimiqljmm.supabase.co:5432/postgres"
        cmd = f'proxychains4 -q pg_dump "{db_uri}" -F c -f /root/supabase_backup.dump'
        
        stdin, stdout, stderr = client.exec_command(cmd)
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            print("Dump SUCCESSFUL!")
            sz_cmd = "ls -lh /root/supabase_backup.dump"
            print("Size:", client.exec_command(sz_cmd)[1].read().decode())
        else:
            print("Dump FAILED!")
            print(stderr.read().decode())
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_ssh()
