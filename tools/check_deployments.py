#!/usr/bin/env python3
"""
Check deployed models (not just available models)
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from tools.azure_ai_client import AzureAIClient

async def check_deployments():
    """Check actual deployed models"""
    async with AzureAIClient() as client:
        # Try different API endpoints to find deployments
        endpoints_to_try = [
            "/openai/deployments",
            "/deployments", 
            "/models/deployments",
            "/openai/models/deployments"
        ]
        
        for endpoint in endpoints_to_try:
            try:
                url = f"{client.config.openai_endpoint.rstrip('/')}{endpoint}"
                params = {'api-version': client.config.openai_version}
                
                print(f"🔍 Trying: {endpoint}")
                response = await client.http_client.get(
                    url, 
                    headers=client._openai_headers(),
                    params=params
                )
                
                if response.is_success:
                    data = response.json()
                    print(f"✅ Found deployments at {endpoint}:")
                    
                    if 'data' in data:
                        deployments = data['data']
                    elif 'value' in data:
                        deployments = data['value']
                    else:
                        deployments = data if isinstance(data, list) else [data]
                    
                    for deployment in deployments:
                        if isinstance(deployment, dict):
                            name = deployment.get('id', deployment.get('name', 'unknown'))
                            model = deployment.get('model', deployment.get('model_id', 'unknown'))
                            status = deployment.get('status', 'unknown')
                            print(f"  🤖 {name} -> {model} (status: {status})")
                    
                    return  # Found it!
                else:
                    print(f"❌ {response.status_code}: {endpoint}")
                    
            except Exception as e:
                print(f"❌ Error trying {endpoint}: {e}")
        
        print("\n🤔 No deployment endpoint found. Let's try a specific model test...")
        
        # Try some common deployment names
        common_models = [
            "gpt-35-turbo", "gpt-4", "gpt-4o", "gpt-35-turbo-16k",
            "text-davinci-003", "gpt-4-turbo", "gpt-4o-mini"
        ]
        
        for model in common_models:
            try:
                url = f"{client.config.openai_endpoint.rstrip('/')}/openai/deployments/{model}/chat/completions"
                params = {'api-version': client.config.openai_version}
                
                # Try a minimal request
                payload = {
                    'messages': [{"role": "user", "content": "test"}],
                    'max_tokens': 5
                }
                
                response = await client.http_client.post(
                    url,
                    headers=client._openai_headers(),
                    params=params,
                    json=payload
                )
                
                if response.status_code != 404:  # Not "deployment not found"
                    print(f"✅ Found working deployment: {model} (status: {response.status_code})")
                    if response.is_success:
                        result = response.json()
                        content = result['choices'][0]['message']['content']
                        print(f"   Test response: {content}")
                    break
                    
            except Exception as e:
                continue  # Try next model
        
        print("\n💡 If no deployments found, you may need to deploy a model in Azure AI Studio first.")

if __name__ == "__main__":
    asyncio.run(check_deployments())