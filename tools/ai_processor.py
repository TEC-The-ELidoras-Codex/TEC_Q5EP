#!/usr/bin/env python3
"""
AI-Enhanced Evidence Processor for TEC_Q5EP
Automatically analyzes and enriches evidence submissions
"""

import asyncio
import json
import sys
from pathlib import Path

# Add parent directory to path  
sys.path.append(str(Path(__file__).parent.parent))
from tools.azure_ai_client import AzureAIClient

async def process_evidence_run(run_id: str):
    """
    Process an existing evidence run with AI analysis
    
    Args:
        run_id: The run ID to process
    """
    
    # Load the run data
    run_path = Path(f"data/runs/{run_id}")
    if not run_path.exists():
        print(f"❌ Run {run_id} not found at {run_path}")
        return
    
    # Read existing metadata and note
    metadata_file = run_path / "metadata.json"
    note_file = run_path / "note.txt"
    
    if not note_file.exists():
        print(f"❌ No note found for run {run_id}")
        return
    
    # Load existing data
    with open(metadata_file) as f:
        metadata = json.load(f)
    
    with open(note_file) as f:
        note_content = f.read()
    
    print(f"🔍 Processing run {run_id}...")
    print(f"📝 Note: {note_content[:100]}...")
    
    # Analyze with AI
    async with AzureAIClient() as client:
        has_photo = (run_path / "photo.jpg").exists()
        analysis = await client.analyze_evidence(
            note=note_content,
            has_photo=has_photo
        )
        
        if analysis and 'analysis' in analysis:
            print(f"🤖 AI Analysis completed")
            
            # Try to parse the JSON analysis
            try:
                # The analysis comes wrapped in markdown code blocks
                analysis_text = analysis['analysis']
                if '```json' in analysis_text:
                    json_start = analysis_text.find('```json') + 7
                    json_end = analysis_text.find('```', json_start)
                    json_str = analysis_text[json_start:json_end].strip()
                    
                    ai_analysis = json.loads(json_str)
                    
                    # Enrich metadata with AI insights
                    metadata['ai_analysis'] = ai_analysis
                    metadata['ai_processed'] = True
                    metadata['ai_relevance_score'] = ai_analysis.get('scientific_relevance', 0)
                    
                    # Merge AI tags with existing tags
                    ai_tags = ai_analysis.get('tags', [])
                    existing_tags = set(metadata.get('tags', []))
                    new_tags = existing_tags.union(set(ai_tags))
                    metadata['tags'] = list(new_tags)
                    
                    # Save enhanced metadata
                    with open(metadata_file, 'w') as f:
                        json.dump(metadata, f, indent=2)
                    
                    print(f"✅ Enhanced metadata saved")
                    print(f"🏷️  Tags: {', '.join(metadata['tags'])}")
                    print(f"⭐ Relevance Score: {metadata['ai_relevance_score']}/10")
                    
                    # Show key insights
                    if 'key_observations_and_patterns' in ai_analysis:
                        print(f"🔬 Key Observations:")
                        observations = ai_analysis['key_observations_and_patterns']
                        if isinstance(observations, dict):
                            for key, value in observations.items():
                                print(f"   • {key.replace('_', ' ').title()}: {value}")
                        elif isinstance(observations, list):
                            for obs in observations:
                                print(f"   • {obs}")
                    
                    if 'suggested_follow_up_actions' in ai_analysis:
                        print(f"🎯 Suggested Actions:")
                        actions = ai_analysis['suggested_follow_up_actions']
                        if isinstance(actions, list):
                            for i, action in enumerate(actions[:3], 1):
                                print(f"   {i}. {action}")
                        else:
                            print(f"   1. {actions}")
                    
                    return True  # Success
                    
            except json.JSONDecodeError as e:
                print(f"⚠️  Could not parse AI analysis as JSON: {e}")
                # Still save the raw analysis
                metadata['ai_analysis_raw'] = analysis['analysis']
                metadata['ai_processed'] = True
                
                with open(metadata_file, 'w') as f:
                    json.dump(metadata, f, indent=2)
        
        else:
            print(f"❌ AI analysis failed")

async def bulk_process_recent_runs(limit: int = 5):
    """Process the most recent runs that haven't been AI-analyzed"""
    
    runs_dir = Path("data/runs")
    if not runs_dir.exists():
        print("❌ No runs directory found")
        return
    
    # Find runs that haven't been AI processed
    unprocessed_runs = []
    
    for run_dir in runs_dir.iterdir():
        if run_dir.is_dir():
            metadata_file = run_dir / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file) as f:
                    metadata = json.load(f)
                
                # Check if already processed
                if not metadata.get('ai_processed', False):
                    unprocessed_runs.append((run_dir.name, metadata.get('timestamp', '0')))
    
    # Sort by timestamp (most recent first)
    unprocessed_runs.sort(key=lambda x: x[1], reverse=True)
    
    print(f"🔍 Found {len(unprocessed_runs)} unprocessed runs")
    
    # Process up to limit
    for run_id, _ in unprocessed_runs[:limit]:
        await process_evidence_run(run_id)
        print("-" * 50)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Process specific run
        run_id = sys.argv[1]
        asyncio.run(process_evidence_run(run_id))
    else:
        # Process recent unprocessed runs
        asyncio.run(bulk_process_recent_runs())