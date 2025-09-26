#!/usr/bin/env python3
"""
Check available Azure OpenAI models
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from tools.azure_ai_client import AzureAIClient

async def list_models():
    """List available models in Azure OpenAI"""
    async with AzureAIClient() as client:
        url = f"{client.config.openai_endpoint.rstrip('/')}/openai/models"
        params = {'api-version': client.config.openai_version}
        
        response = await client.http_client.get(
            url, 
            headers=client._openai_headers(),
            params=params
        )
        
        if response.is_success:
            models = response.json()['data']
            print(f"📋 Available Models ({len(models)} total):")
            print("=" * 50)
            
            for model in models:
                model_id = model.get('id', 'unknown')
                status = model.get('status', 'unknown')
                print(f"🤖 {model_id} (status: {status})")
            
            # Filter for chat models
            chat_models = [m for m in models if 'gpt' in m.get('id', '').lower()]
            if chat_models:
                print(f"\n💬 Chat Models ({len(chat_models)}):")
                for model in chat_models[:10]:  # Show first 10
                    print(f"  • {model.get('id')}")
        else:
            print(f"❌ Failed to get models: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    asyncio.run(list_models())