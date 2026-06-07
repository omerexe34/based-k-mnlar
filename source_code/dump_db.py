import paramiko

def run_ssh():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Connecting to VPS to run pg_dump...")
        client.connect(
            hostname="89.47.113.37",
            username="root",
            password="StQCqZUfpyPp1_",
            timeout=10
        )
        print("Connected! Running pg_dump (this might take a minute)...")
        
        # Install postgresql-client if not exists to get pg_dump
        stdin, stdout, stderr = client.exec_command("apt-get update && apt-get install -y postgresql-client")
        stdout.channel.recv_exit_status()
        
        # Run pg_dump
        db_uri = "postgresql://postgres:jytrfvbnjuytrfvbn@db.xrzepgacyugeimiqljmm.supabase.co:5432/postgres"
        cmd = f'pg_dump "{db_uri}" -F c -f /root/supabase_backup.dump'
        stdin, stdout, stderr = client.exec_command(cmd)
        
        # Wait for the command to finish
        exit_status = stdout.channel.recv_exit_status()
        
        if exit_status == 0:
            print("Database dumped successfully on VPS.")
            stdin, stdout, stderr = client.exec_command("ls -lh /root/supabase_backup.dump")
            print("Backup file size:", stdout.read().decode())
        else:
            print("Error dumping database:")
            print(stderr.read().decode())
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_ssh()
