#!/usr/bin/env python3
"""
Quick Azure AI test with working model
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from tools.azure_ai_client import AzureAIClient

async def quick_test():
    """Quick test with gpt-35-turbo"""
    async with AzureAIClient() as client:
        
        # Test 1: Simple chat
        print("🤖 Testing GPT-4o Mini (deployed model)...")
        try:
            messages = [
                {"role": "system", "content": "You are a helpful AI assistant for TEC_Q5EP research."},
                {"role": "user", "content": "Hello! Can you help analyze evidence submissions for resonance research?"}
            ]
            
            response = await client.chat_completion(messages)  # Uses default deployed model
            if response:
                content = response['choices'][0]['message']['content']
                print(f"✅ Success: {content[:100]}...")
            else:
                print("❌ No response")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test 2: Evidence analysis
        print("\n🔬 Testing Evidence Analysis...")
        try:
            analysis = await client.analyze_evidence(
                "Observed strange resonance patterns in crystalline water structure during lunar phase transition. Temperature remained constant at 21.5°C, but the formation patterns were highly unusual - geometric, almost fractal-like structures appeared.",
                has_photo=True
            )
            print(f"📊 Analysis: {json.dumps(analysis, indent=2)}")
        except Exception as e:
            print(f"❌ Analysis error: {e}")

if __name__ == "__main__":
    asyncio.run(quick_test())