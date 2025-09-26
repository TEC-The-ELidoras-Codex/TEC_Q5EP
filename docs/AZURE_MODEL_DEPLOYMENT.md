# Azure AI Model Deployment Instructions

## Quick Deploy via Azure Portal

1. **Go to Azure AI Studio**: <https://ai.azure.com/>
2. **Find your resource**: Navigate to "tecagent" resource
3. **Go to Model Deployments**: Left sidebar → "Deployments"
4. **Create New Deployment**:
   - Click "+ Create deployment"
   - Choose model: **GPT-4o mini** (cost-effective, fast)
   - Deployment name: `gpt-4o-mini-deploy`
   - Click "Deploy"

## Alternative: Deploy via Azure Portal

1. **Go to Azure Portal**: <https://portal.azure.com/>
2. **Find Azure OpenAI**: Search "Azure OpenAI" → Select your "tecagent" resource
3. **Model Deployments**: Left menu → "Model deployments"
4. **Manage Deployments**: Click "Manage Deployments" (opens AI Studio)
5. **Deploy GPT-4o mini** as above

## Recommended First Deployment

Model: **GPT-4o mini**

- ✅ Cost-effective ($0.15/1M input tokens)
- ✅ Fast response times
- ✅ Good for evidence analysis
- ✅ Supports JSON mode
- ✅ 128k context window

## After Deployment

Once deployed, update this file with the deployment name:

```
# In your .env file, add:
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini-deploy
```

Then test with:

```bash
./.venv/Scripts/python.exe tools/test_ai.py
```

## PowerShell Automation (Alternative)

If you have Azure CLI installed:

```powershell
# Login to Azure
az login

# Deploy GPT-4o mini
az cognitiveservices account deployment create \
  --resource-group "your-resource-group" \
  --account-name "tecagent" \
  --deployment-name "gpt-4o-mini-deploy" \
  --model-name "gpt-4o-mini" \
  --model-version "2024-07-18" \
  --model-format "OpenAI" \
  --sku-capacity 10 \
  --sku-name "Standard"
```

Replace `your-resource-group` with your actual resource group name.

## Next Steps After Deployment

1. ✅ Deploy model (you're doing this now)
2. 🔄 Update .env with deployment name
3. 🧪 Test AI integration
4. 🚀 Integrate with TEC evidence pipeline
5. 🎯 Build automated post generation
