import paramiko

def deploy():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect("89.47.113.37", username="root", password="StQCqZUfpyPp1_", timeout=10)
        
        setup_script = f"""
        cd /var/www/freerider
        ./venv/bin/pip install -r requirements.txt --quiet
        ./venv/bin/pip install gunicorn python-dotenv flask-cors --quiet
        
        systemctl daemon-reload
        systemctl enable freerider
        systemctl restart freerider
        systemctl status freerider --no-pager
        """
        
        stdin, stdout, stderr = client.exec_command(setup_script)
        
        # Read properly ignoring charmap issues
        print(stdout.read().decode('utf-8', errors='replace'))
        print(stderr.read().decode('utf-8', errors='replace'))
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    deploy()
