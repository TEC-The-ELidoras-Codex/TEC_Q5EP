#!/usr/bin/env python3
"""
Azure AI Client for TEC_Q5EP
Provides unified access to Azure OpenAI, Speech, Translation services
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class AzureAIConfig:
    """Configuration for Azure AI services"""
    openai_endpoint: str
    openai_key: str
    openai_version: str
    foundry_endpoint: str
    foundry_key: str
    speech_stt_endpoint: str
    speech_tts_endpoint: str
    translator_endpoint: str
    
    @classmethod
    def from_env(cls) -> 'AzureAIConfig':
        """Load configuration from environment variables"""
        return cls(
            openai_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT', ''),
            openai_key=os.getenv('AZURE_OPENAI_KEY', ''),
            openai_version=os.getenv('AZURE_OPENAI_VERSION', '2024-05-01-preview'),
            foundry_endpoint=os.getenv('AZURE_AI_FOUNDRY_ENDPOINT', ''),
            foundry_key=os.getenv('AZURE_AI_FOUNDRY_KEY', ''),
            speech_stt_endpoint=os.getenv('AZURE_SPEECH_STT_ENDPOINT', ''),
            speech_tts_endpoint=os.getenv('AZURE_SPEECH_TTS_ENDPOINT', ''),
            translator_endpoint=os.getenv('AZURE_TRANSLATOR_ENDPOINT', ''),
        )


class AzureAIClient:
    """Unified client for Azure AI services"""
    
    def __init__(self, config: Optional[AzureAIConfig] = None):
        self.config = config or AzureAIConfig.from_env()
        self.http_client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close the HTTP client"""
        await self.http_client.aclose()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
    
    def _openai_headers(self) -> Dict[str, str]:
        """Get headers for OpenAI API calls"""
        return {
            'api-key': self.config.openai_key,
            'Content-Type': 'application/json'
        }
    
    def _foundry_headers(self) -> Dict[str, str]:
        """Get headers for AI Foundry API calls"""
        return {
            'api-key': self.config.foundry_key,
            'Content-Type': 'application/json'
        }
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test connection to all configured services"""
        results = {}
        
        # Test OpenAI endpoint
        try:
            url = f"{self.config.openai_endpoint.rstrip('/')}/openai/models"
            params = {'api-version': self.config.openai_version}
            response = await self.http_client.get(
                url, 
                headers=self._openai_headers(),
                params=params
            )
            results['openai'] = {
                'status': response.status_code,
                'success': response.is_success,
                'models_count': len(response.json().get('data', [])) if response.is_success else 0
            }
        except Exception as e:
            results['openai'] = {'status': 'error', 'error': str(e)}
        
        # Test AI Foundry endpoint
        try:
            url = f"{self.config.foundry_endpoint.rstrip('/')}/agents"
            response = await self.http_client.get(
                url,
                headers=self._foundry_headers()
            )
            results['foundry'] = {
                'status': response.status_code,
                'success': response.is_success
            }
        except Exception as e:
            results['foundry'] = {'status': 'error', 'error': str(e)}
        
        return results
    
    async def chat_completion(self, 
                            messages: List[Dict[str, str]], 
                            model: Optional[str] = None,
                            temperature: float = 0.7,
                            max_tokens: int = 1000) -> Optional[Dict[str, Any]]:
        """Generate chat completion using Azure OpenAI"""
        # Use deployment name from env or default to our deployed model
        deployment_name = model or os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'gpt-4o-mini')
        
        url = f"{self.config.openai_endpoint.rstrip('/')}/openai/deployments/{deployment_name}/chat/completions"
        params = {'api-version': self.config.openai_version}
        
        payload = {
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        
        response = await self.http_client.post(
            url,
            headers=self._openai_headers(),
            params=params,
            json=payload
        )
        
        if response.is_success:
            return response.json()
        else:
            response.raise_for_status()
    
    async def generate_summary(self, text: str) -> str:
        """Generate a summary of the provided text"""
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that creates concise summaries. Focus on key insights and actionable information."
            },
            {
                "role": "user", 
                "content": f"Please provide a concise summary of the following text:\n\n{text}"
            }
        ]
        
        try:
            result = await self.chat_completion(messages, max_tokens=200)
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    async def analyze_evidence(self, note: str, has_photo: bool = False) -> Dict[str, Any]:
        """Analyze evidence submission for TEC research patterns"""
        messages = [
            {
                "role": "system",
                "content": """You are an AI assistant helping with TEC (The Elidoras Codex) research on Resonance phenomena. 
                Analyze evidence submissions and identify:
                1. Key observations and patterns
                2. Resonance-related themes
                3. Scientific relevance (1-10 scale)
                4. Suggested follow-up actions
                5. Tags for categorization
                
                Return analysis in JSON format."""
            },
            {
                "role": "user",
                "content": f"""Analyze this evidence submission:
                
                Note: {note}
                Has Photo: {has_photo}
                
                Please provide structured analysis."""
            }
        ]
        
        try:
            result = await self.chat_completion(messages, max_tokens=500)
            content = result['choices'][0]['message']['content'].strip()
            
            # Try to parse as JSON, fallback to structured text
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {
                    "analysis": content,
                    "error": "Could not parse as JSON"
                }
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}


async def main():
    """Test the Azure AI client"""
    print("🔧 Testing Azure AI Connection...")
    
    async with AzureAIClient() as client:
        # Test connection
        results = await client.test_connection()
        print(f"📊 Connection Test Results:")
        for service, result in results.items():
            status = "✅" if result.get('success') else "❌"
            print(f"  {status} {service.title()}: {result}")
        
        # Test chat completion if OpenAI is working
        if results.get('openai', {}).get('success'):
            print("\n💭 Testing Chat Completion...")
            try:
                response = await client.chat_completion([
                    {"role": "user", "content": "Say hello to TEC_Q5EP! What can you help with?"}
                ])
                print(f"🤖 AI Response: {response['choices'][0]['message']['content']}")
            except Exception as e:
                print(f"❌ Chat test failed: {e}")
        
        # Test evidence analysis
        print("\n🔬 Testing Evidence Analysis...")
        try:
            analysis = await client.analyze_evidence(
                "Observed unusual resonance patterns in water crystals during full moon. Temperature stable at 22°C.",
                has_photo=True
            )
            print(f"📈 Analysis Result: {json.dumps(analysis, indent=2)}")
        except Exception as e:
            print(f"❌ Analysis test failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())