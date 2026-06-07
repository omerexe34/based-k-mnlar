import paramiko
import os

def run_ssh():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect("89.47.113.37", username="root", password="StQCqZUfpyPp1_", timeout=10)
        
        sftp = client.open_sftp()
        local_path = "auth_users_backup.csv"
        remote_path = "/root/auth_users_backup.csv"
        
        print("Uploading...")
        sftp.put(local_path, remote_path)
        print("Done!")
        
        sftp.close()
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    run_ssh()
