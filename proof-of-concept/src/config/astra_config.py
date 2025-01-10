from cassandra.auth import PlainTextAuthProvider
import json
import os

class AstraDBConfig:
    def __init__(self):
        # Path to the token file
        token_path = "db_creds/social_media_performance_analysis_db-token.json"
        
        # Validate token file exists
        if not os.path.exists(token_path):
            raise FileNotFoundError(f"Token file not found: {token_path}")
            
        # Read credentials from token file
        try:
            with open(token_path) as f:
                secrets = json.load(f)
                
            self.client_id = secrets["clientId"]
            self.client_secret = secrets["secret"]
            
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Invalid token file format: {str(e)}")
        
        # Set up the cloud configuration
        self.cloud_config = {
            'secure_connect_bundle': 'db_creds/secure-connect-social-media-performance-analysis-db.zip'
        }
        
        # Create the auth provider with credentials from token file
        self.auth_provider = PlainTextAuthProvider(
            username=self.client_id,
            password=self.client_secret
        )

    def get_auth_provider(self):
        """Return the configured auth provider"""
        return self.auth_provider

    def get_cloud_config(self):
        """Return the cloud configuration"""
        return self.cloud_config