import paramiko
import os

def deploy():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Connecting to VPS...")
        client.connect("89.47.113.37", username="root", password="StQCqZUfpyPp1_", timeout=10)
        
        # Get Supabase keys from the VPS docker .env
        print("Getting Supabase keys...")
        stdin, stdout, stderr = client.exec_command("grep -E 'ANON_KEY=|SERVICE_ROLE_KEY=' /root/supabase/docker/.env")
        env_vars = stdout.read().decode().splitlines()
        
        anon_key = ""
        service_role = ""
        for line in env_vars:
            if line.startswith("ANON_KEY="): anon_key = line.split("=", 1)[1]
            if line.startswith("SERVICE_ROLE_KEY="): service_role = line.split("=", 1)[1]
            
        supa_url = "http://127.0.0.1:8000"
        
        sftp = client.open_sftp()
        print("Uploading app...")
        sftp.put("app_deployment.zip", "/root/app_deployment.zip")
        sftp.close()
        
        setup_script = f"""
        apt-get install -y unzip python3-venv python3-pip
        mkdir -p /var/www/freerider
        cd /var/www/freerider
        unzip -o /root/app_deployment.zip
        
        echo "SUPABASE_URL={supa_url}" > .env
        echo "SUPABASE_KEY={anon_key}" >> .env
        echo "SERVICE_ROLE_KEY={service_role}" >> .env
        
        python3 -m venv venv
        ./venv/bin/pip install -r requirements.txt
        ./venv/bin/pip install gunicorn python-dotenv flask-cors
        
        cat << 'EOF' > /etc/systemd/system/freerider.service
[Unit]
Description=Gunicorn instance to serve FreeriderTR
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/freerider
Environment="PATH=/var/www/freerider/venv/bin"
EnvironmentFile=/var/www/freerider/.env
ExecStart=/var/www/freerider/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 -m 007 app:app

[Install]
WantedBy=multi-user.target
EOF

        systemctl daemon-reload
        systemctl enable freerider
        systemctl restart freerider
        
        echo "Deployment complete! App is running on port 5000"
        """
        
        print("Running setup on VPS...")
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
    deploy()
