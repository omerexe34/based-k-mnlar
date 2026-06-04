import paramiko

def run_ssh():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    regions = [
        "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", 
        "eu-north-1", "eu-south-1",
        "us-east-1", "us-east-2", "us-west-1", "us-west-2",
        "ap-south-1", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1", "ap-northeast-2",
        "sa-east-1", "ca-central-1"
    ]
    
    try:
        client.connect("89.47.113.37", username="root", password="StQCqZUfpyPp1_", timeout=10)
        
        for region in regions:
            host = f"aws-0-{region}.pooler.supabase.com"
            db_uri = f"postgresql://postgres.xrzepgacyugeimiqljmm:jytrfvbnjuytrfvbn@{host}:6543/postgres"
            
            # Use psql to check connection. -c "SELECT 1;"
            cmd = f'psql "{db_uri}" -c "SELECT 1;"'
            stdin, stdout, stderr = client.exec_command(cmd)
            exit_status = stdout.channel.recv_exit_status()
            
            err = stderr.read().decode().strip()
            out = stdout.read().decode().strip()
            
            if "ENOTFOUND" not in err and "could not translate host name" not in err:
                print(f"Region {region} output:")
                print("OUT:", out)
                print("ERR:", err)
                if exit_status == 0:
                    print(f"FOUND EXACT REGION: {region}")
                    print("Starting dump...")
                    dump_cmd = f'pg_dump "{db_uri}" -F c -f /root/supabase_backup.dump'
                    client.exec_command(dump_cmd).stdout.channel.recv_exit_status()
                    print("Dump finished!")
                    return
        print("Could not find the region.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_ssh()
