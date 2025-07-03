#!/usr/bin/env python3
"""
OAuth Manager for Google MCP Security Agent

This script manages OAuth operations for AgentSpace integration,
including client creation guidance, authorization URI generation,
and linking OAuth to AgentSpace.
"""

import os
import sys
import json
import subprocess
import webbrowser
from pathlib import Path
from typing import Dict, Optional, Tuple
from urllib.parse import urlencode
import argparse
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))
from scripts.env_manager import EnvManager


class OAuthManager:
    """Manages OAuth configuration and operations."""
    
    OAUTH_CONSOLE_URL = "https://console.cloud.google.com/apis/credentials"
    REDIRECT_URI = "https://vertexaisearch.cloud.google.com/oauth-redirect"
    TOKEN_URI = "https://oauth2.googleapis.com/token"
    
    def __init__(self, env_file: str = '.env'):
        """Initialize the OAuth manager."""
        self.env_manager = EnvManager(env_file)
        self.env_vars = self.env_manager.env_vars
        
    def guide_client_creation(self) -> None:
        """Guide user through OAuth client creation process."""
        print("=" * 60)
        print("OAuth Client Creation Guide")
        print("=" * 60)
        print()
        
        project = self.env_vars.get('GOOGLE_CLOUD_PROJECT')
        if not project:
            print("⚠️  Warning: GOOGLE_CLOUD_PROJECT not set in .env")
            print("   Please set it first: make env-update KEY=GOOGLE_CLOUD_PROJECT VALUE=<project-id>")
            print()
        
        print("Steps to create an OAuth 2.0 client:")
        print()
        print("1. Open the Google Cloud Console:")
        print(f"   {self.OAUTH_CONSOLE_URL}")
        if project:
            print(f"   (Make sure you're in project: {project})")
        print()
        
        print("2. Click '+ CREATE CREDENTIALS' → 'OAuth client ID'")
        print()
        
        print("3. If prompted to configure consent screen:")
        print("   - Choose 'Internal' for organization use")
        print("   - Fill in required fields")
        print("   - Add scopes if needed")
        print()
        
        print("4. For Application type, select 'Web application'")
        print()
        
        print("5. Configure the client:")
        print("   - Name: 'AgentSpace MCP Security Agent' (or similar)")
        print("   - Authorized redirect URIs:")
        print(f"     {self.REDIRECT_URI}")
        print()
        
        print("6. Click 'CREATE'")
        print()
        
        print("7. Download the client configuration:")
        print("   - Click the download button (⬇) next to your new client")
        print("   - Save as 'client_secret.json' in this directory")
        print()
        
        # Offer to open the console
        response = input("Would you like to open the Google Cloud Console now? (y/n): ")
        if response.lower() == 'y':
            webbrowser.open(self.OAUTH_CONSOLE_URL)
            print("\n✓ Opened Google Cloud Console in your browser")
        
        print("\nOnce you've downloaded the client_secret.json file:")
        print("Run: make oauth-uri")
        
    def generate_auth_uri(self, client_secret_path: Optional[str] = None) -> str:
        """Generate OAuth authorization URI."""
        # Use provided path or look for client_secret.json
        if not client_secret_path:
            client_secret_path = 'client_secret.json'
        
        if not Path(client_secret_path).exists():
            print(f"Error: Client secret file not found: {client_secret_path}")
            print("\nPlease run 'make oauth-client' to create an OAuth client first.")
            sys.exit(1)
        
        # Load client configuration
        with open(client_secret_path, 'r') as f:
            client_data = json.load(f)
        
        # Extract client configuration
        if 'web' in client_data:
            client_config = client_data['web']
        elif 'installed' in client_data:
            client_config = client_data['installed']
        else:
            raise ValueError("Invalid client_secret.json format")
        
        client_id = client_config['client_id']
        client_secret = client_config['client_secret']
        auth_uri = client_config.get('auth_uri', 'https://accounts.google.com/o/oauth2/v2/auth')
        
        # Update environment variables
        self.env_manager.update_env('OAUTH_CLIENT_ID', client_id)
        self.env_manager.update_env('OAUTH_CLIENT_SECRET', client_secret)
        self.env_manager.update_env('OAUTH_TOKEN_URI', self.TOKEN_URI)
        
        # Get or generate auth ID
        auth_id = self.env_vars.get('OAUTH_AUTH_ID')
        if not auth_id:
            auth_id = f"mcp-agent-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            self.env_manager.update_env('OAUTH_AUTH_ID', auth_id)
            print(f"Generated AUTH_ID: {auth_id}")
        
        # Get redirect URI and scopes
        redirect_uri = self.env_vars.get('OAUTH_REDIRECT_URI', self.REDIRECT_URI)
        scopes = self.env_vars.get('OAUTH_SCOPES', 
            'https://www.googleapis.com/auth/cloud-platform,'
            'https://www.googleapis.com/auth/generative-language.retriever'
        ).split(',')
        
        # OAuth parameters
        params = {
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': ' '.join(scopes),
            'access_type': 'offline',
            'prompt': 'consent'
        }
        
        # Generate authorization URL
        auth_url = f"{auth_uri}?{urlencode(params)}"
        
        # Save to environment
        self.env_manager.update_env('OAUTH_AUTH_URI', auth_url)
        
        print("\n✓ OAuth configuration updated in .env")
        print("\nOAuth Authorization URI:")
        print("=" * 80)
        print(auth_url)
        print("=" * 80)
        print("\nNext steps:")
        print("1. Open the above URL in your browser")
        print("2. Sign in and grant permissions")
        print("3. After redirect, run: make oauth-link")
        
        return auth_url
    
    def link_to_agentspace(self) -> bool:
        """Link OAuth authorization to AgentSpace."""
        # Validate required variables
        required = [
            'AGENTSPACE_PROJECT_NUMBER',
            'OAUTH_CLIENT_ID',
            'OAUTH_CLIENT_SECRET',
            'OAUTH_AUTH_ID',
            'OAUTH_AUTH_URI'
        ]
        
        missing = [var for var in required if not self.env_vars.get(var)]
        if missing:
            print("Error: Missing required environment variables:")
            for var in missing:
                print(f"  - {var}")
            print("\nPlease set these variables in your .env file")
            return False
        
        project_number = self.env_vars['AGENTSPACE_PROJECT_NUMBER']
        auth_id = self.env_vars['OAUTH_AUTH_ID']
        
        # Prepare API request
        api_url = (
            f"https://discoveryengine.googleapis.com/v1alpha/"
            f"projects/{project_number}/locations/global/authorizations"
            f"?authorizationId={auth_id}"
        )
        
        payload = {
            "name": f"projects/{project_number}/locations/global/authorizations/{auth_id}",
            "serverSideOauth2": {
                "clientId": self.env_vars['OAUTH_CLIENT_ID'],
                "clientSecret": self.env_vars['OAUTH_CLIENT_SECRET'],
                "authorizationUri": self.env_vars['OAUTH_AUTH_URI'],
                "tokenUri": self.env_vars.get('OAUTH_TOKEN_URI', self.TOKEN_URI)
            }
        }
        
        # Create the authorization
        print(f"Creating OAuth authorization '{auth_id}' in AgentSpace...")
        
        try:
            # Get access token
            token_result = subprocess.run(
                ['gcloud', 'auth', 'print-access-token'],
                capture_output=True,
                text=True,
                check=True
            )
            access_token = token_result.stdout.strip()
            
            # Make API request
            import requests
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                'X-Goog-User-Project': project_number
            }
            
            response = requests.post(api_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                print("\n✓ OAuth authorization created successfully!")
                print(f"  Authorization ID: {auth_id}")
                print("\nNext steps:")
                print("1. Deploy your agent: make adk-deploy")
                print("2. Register with AgentSpace: make agentspace-register")
                return True
            else:
                print(f"\n✗ Failed to create authorization: {response.status_code}")
                print(f"  Response: {response.text}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"\n✗ Failed to get access token: {e}")
            print("  Make sure you're authenticated: gcloud auth login")
            return False
        except Exception as e:
            print(f"\n✗ Error creating authorization: {e}")
            return False
    
    def verify_oauth(self) -> bool:
        """Verify OAuth configuration and authorization."""
        print("Verifying OAuth configuration...")
        print()
        
        # Check client configuration
        client_vars = ['OAUTH_CLIENT_ID', 'OAUTH_CLIENT_SECRET']
        client_ok = all(self.env_vars.get(var) for var in client_vars)
        
        if client_ok:
            print("✓ OAuth client configured")
            print(f"  Client ID: {self.env_vars['OAUTH_CLIENT_ID'][:20]}...")
        else:
            print("✗ OAuth client not configured")
            print("  Run: make oauth-client")
            return False
        
        # Check authorization
        if self.env_vars.get('OAUTH_AUTH_ID'):
            print(f"✓ OAuth authorization ID: {self.env_vars['OAUTH_AUTH_ID']}")
        else:
            print("✗ OAuth authorization not created")
            print("  Run: make oauth-uri")
            return False
        
        # Check AgentSpace link
        if self.env_vars.get('AGENTSPACE_PROJECT_NUMBER'):
            # Try to verify the authorization exists
            project_number = self.env_vars['AGENTSPACE_PROJECT_NUMBER']
            auth_id = self.env_vars['OAUTH_AUTH_ID']
            
            try:
                token_result = subprocess.run(
                    ['gcloud', 'auth', 'print-access-token'],
                    capture_output=True,
                    text=True,
                    check=True
                )
                access_token = token_result.stdout.strip()
                
                import requests
                api_url = (
                    f"https://discoveryengine.googleapis.com/v1alpha/"
                    f"projects/{project_number}/locations/global/authorizations/{auth_id}"
                )
                
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'X-Goog-User-Project': project_number
                }
                
                response = requests.get(api_url, headers=headers)
                
                if response.status_code == 200:
                    print("✓ OAuth linked to AgentSpace")
                else:
                    print("✗ OAuth not linked to AgentSpace")
                    print("  Run: make oauth-link")
                    return False
                    
            except Exception:
                print("⚠️  Could not verify AgentSpace link")
        else:
            print("⚠️  AgentSpace not configured")
        
        print("\n✓ OAuth configuration verified")
        return True


def main():
    """Main entry point for CLI usage."""
    parser = argparse.ArgumentParser(description='Manage OAuth configuration')
    parser.add_argument('action', choices=['guide', 'generate', 'link', 'verify'],
                       help='Action to perform')
    parser.add_argument('--client-secret', help='Path to client_secret.json')
    parser.add_argument('--env-file', default='.env', help='Environment file to use')
    
    args = parser.parse_args()
    
    manager = OAuthManager(args.env_file)
    
    if args.action == 'guide':
        manager.guide_client_creation()
    
    elif args.action == 'generate':
        manager.generate_auth_uri(args.client_secret)
    
    elif args.action == 'link':
        if manager.link_to_agentspace():
            sys.exit(0)
        else:
            sys.exit(1)
    
    elif args.action == 'verify':
        if manager.verify_oauth():
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == '__main__':
    main()