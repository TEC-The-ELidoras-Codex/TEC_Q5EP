#!/usr/bin/env python3
"""
TEC_Q5EP Codex Setup Verification
Checks that all components are properly configured
"""
import os
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

def check_environment():
    """Check environment variable setup"""
    print("🔧 Environment Configuration")
    load_dotenv()
    
    required_keys = [
        "OPENAI_API_KEY",
        "AZURE_OPENAI_API_KEY", 
        "XAI_API_KEY",
        "GITHUB_TOKEN",
        "HF_API_KEY",
        "ANTHROPIC_API_KEY"
    ]
    
    for key in required_keys:
        value = os.getenv(key)
        if value and len(value) > 10:  # Check for reasonable length
            print(f"   ✅ {key}: {value[:8]}...")
        else:
            print(f"   ❌ {key}: Missing or incomplete")
    print()

def check_codex_config():
    """Check Codex configuration file"""
    print("📋 Codex Configuration")
    config_path = Path.home() / ".codex" / "config.toml"
    
    if config_path.exists():
        print(f"   ✅ Config file exists: {config_path}")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if "tec-auto" in content:
                    print("   ✅ TEC profiles configured")
                if "openai" in content and "azure" in content:
                    print("   ✅ Multi-provider setup detected")
        except UnicodeDecodeError:
            print("   ⚠️ Config file has encoding issues, but exists")
    else:
        print(f"   ❌ Config file missing: {config_path}")
    print()

def check_agent_manifest():
    """Check Airth agent manifest"""
    print("🤖 Agent Manifest")
    manifest_path = Path("agents/manifests/airth_research_guard.json")
    
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            data = json.load(f)
            version = data['metadata']['version']
            platforms = data['deployment']['platforms']
            print(f"   ✅ Airth Research Guard v{version}")
            print(f"   ✅ Platforms: {', '.join(platforms)}")
    else:
        print(f"   ❌ Agent manifest missing: {manifest_path}")
    print()

def check_vscode_config():
    """Check VS Code configuration"""
    print("💻 VS Code Configuration")
    launch_path = Path(".vscode/launch.json")
    
    if launch_path.exists():
        print("   ✅ Debug configurations available")
        with open(launch_path, 'r') as f:
            content = f.read()
            if "envFile" in content:
                print("   ✅ Environment file integration configured")
    else:
        print("   ❌ VS Code launch.json missing")
    
    env_example = Path(".env.example")
    if env_example.exists():
        print("   ✅ Environment template available")
    print()

def main():
    """Main verification routine"""
    print("🌟 TEC_Q5EP Codex Setup Verification")
    print("=" * 50)
    
    check_environment()
    check_codex_config()
    check_agent_manifest()
    check_vscode_config()
    
    print("🚀 Quick Start Commands")
    print("   codex --profile tec-auto      # Auto-approval mode")
    print("   codex --profile tec-azure     # Fast Azure 4o-mini")
    print("   codex --profile tec-reason    # High reasoning (o3)")
    print("   codex --profile grok          # xAI Grok-2")
    print()
    print("💡 Next Steps:")
    print("   1. Rotate your API keys and update .env")
    print("   2. Test a profile: codex --profile tec-auto")
    print("   3. Run the API: .venv/Scripts/python.exe -m uvicorn server.app:app --reload")

if __name__ == "__main__":
    main()