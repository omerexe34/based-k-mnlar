import paramiko
import os

def run_ssh():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print("Connecting to VPS...")
        client.connect("89.47.113.37", username="root", password="StQCqZUfpyPp1_", timeout=10)
        sftp = client.open_sftp()
        
        schemas = ["bike_competitions_schema.sql", "giveaways_schema.sql", "supabase_schema_complete.sql"]
        for schema in schemas:
            print(f"Uploading {schema}...")
            sftp.put(schema, f"/root/{schema}")
            
        # Also ensure auth_users_backup.csv is in the right place
        # Copy files to supabase-db container and run them
        
        setup_script = """
        docker cp /root/supabase_schema_complete.sql supabase-db:/tmp/
        docker cp /root/bike_competitions_schema.sql supabase-db:/tmp/
        docker cp /root/giveaways_schema.sql supabase-db:/tmp/
        docker cp /root/auth_users_backup.csv supabase-db:/tmp/
        
        echo "Applying schemas..."
        docker exec supabase-db psql -U postgres -d postgres -f /tmp/supabase_schema_complete.sql
        docker exec supabase-db psql -U postgres -d postgres -f /tmp/bike_competitions_schema.sql
        docker exec supabase-db psql -U postgres -d postgres -f /tmp/giveaways_schema.sql
        
        echo "Importing auth users..."
        docker exec supabase-db psql -U postgres -d postgres -c "\\copy auth.users FROM '/tmp/auth_users_backup.csv' DELIMITER ',' CSV HEADER;"
        """
        
        print("Running database setup on VPS...")
        stdin, stdout, stderr = client.exec_command(setup_script)
        
        for line in iter(stdout.readline, ""):
            print(line, end="")
        
        print("STDERR:")
        for line in iter(stderr.readline, ""):
            print(line, end="")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'sftp' in locals():
            sftp.close()
        client.close()

if __name__ == "__main__":
    run_ssh()
