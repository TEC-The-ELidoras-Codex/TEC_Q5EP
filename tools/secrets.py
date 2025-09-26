#!/usr/bin/env python3
"""
TEC Secrets Manager - Bitwarden integration
Fetches secrets from Bitwarden Secrets Manager and loads them into environment
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional


def get_bw_secret(secret_name: str, access_token: Optional[str] = None) -> Optional[str]:
    """
    Fetch a secret from Bitwarden Secrets Manager
    
    Args:
        secret_name: Name of the secret in Bitwarden
        access_token: BW access token (defaults to env var)
    
    Returns:
        Secret value or None if not found
    """
    token = access_token or os.environ.get("BW_ACCESS_TOKEN")
    if not token:
        print("ERROR: BW_ACCESS_TOKEN not set", file=sys.stderr)
        return None
    
    try:
        cmd = ["bw", "sm", "get", "secret", secret_name, "--access-token", token]
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to fetch secret '{secret_name}': {e.stderr}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("ERROR: Bitwarden CLI not found. Run: winget install Bitwarden.CLI", file=sys.stderr)
        return None


def load_secrets_to_env() -> Dict[str, str]:
    """
    Load secrets from Bitwarden into environment variables
    
    Returns:
        Dictionary of loaded secrets
    """
    secrets_map = {
        "AZURE_OPENAI_KEY": "TEC_AZURE_OPENAI_KEY",
        "AZURE_OPENAI_ENDPOINT": "TEC_AZURE_OPENAI_ENDPOINT", 
        "API_KEY": "TEC_API_SECRET_KEY"
    }
    
    loaded = {}
    for env_var, bw_secret_name in secrets_map.items():
        value = get_bw_secret(bw_secret_name)
        if value:
            os.environ[env_var] = value
            loaded[env_var] = "***loaded***"
        else:
            print(f"WARNING: Could not load {env_var} from {bw_secret_name}", file=sys.stderr)
    
    return loaded


def create_env_file() -> None:
    """
    Create .env file from Bitwarden secrets
    """
    env_path = Path(".env")
    secrets = [
        ("AZURE_OPENAI_KEY", "TEC_AZURE_OPENAI_KEY"),
        ("AZURE_OPENAI_ENDPOINT", "TEC_AZURE_OPENAI_ENDPOINT"),
        ("API_KEY", "TEC_API_SECRET_KEY")
    ]
    
    with env_path.open("w") as f:
        f.write("# Auto-generated from Bitwarden Secrets Manager\n")
        f.write(f"# Generated on: {__import__('datetime').datetime.now().isoformat()}\n\n")
        
        for env_var, bw_secret_name in secrets:
            value = get_bw_secret(bw_secret_name)
            if value:
                f.write(f"{env_var}={value}\n")
            else:
                f.write(f"# {env_var}=<not found in Bitwarden: {bw_secret_name}>\n")
        
        f.write("\n# Static configuration\n")
        f.write("ENVIRONMENT=development\n")
        f.write("DEBUG=true\n")
        f.write("API_HOST=localhost\n")
        f.write("API_PORT=8000\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "create-env":
            create_env_file()
            print("Created .env file from Bitwarden secrets")
        else:
            # Get specific secret
            secret = get_bw_secret(sys.argv[1])
            if secret:
                print(secret)
            else:
                sys.exit(1)
    else:
        # Load all secrets to environment
        loaded = load_secrets_to_env()
        print(f"Loaded {len(loaded)} secrets:", loaded)