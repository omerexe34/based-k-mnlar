import paramiko

def run_ssh():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect("89.47.113.37", username="root", password="StQCqZUfpyPp1_", timeout=10)
        stdin, stdout, stderr = client.exec_command("docker ps")
        print(stdout.read().decode())
    except Exception as e:
        print(e)
    finally:
        client.close()

if __name__ == "__main__":
    run_ssh()
