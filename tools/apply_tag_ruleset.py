#!/usr/bin/env python3
"""
Apply GitHub Tag Ruleset via API

This script helps you apply tag protection rulesets to your GitHub repository
using the GitHub REST API.

Usage:
    python tools/apply_tag_ruleset.py --help
    python tools/apply_tag_ruleset.py --token YOUR_TOKEN --repo OWNER/REPO
    python tools/apply_tag_ruleset.py --token YOUR_TOKEN --repo OWNER/REPO --ruleset strict-semver
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

try:
    import httpx
except ImportError:
    httpx = None  # Will check later when needed


RULESET_FILES = {
    "standard": ".github/tag-ruleset-release-protection.json",
    "strict-semver": ".github/tag-ruleset-strict-semver.json",
}


def load_ruleset(ruleset_type: str, repo_root: Path) -> dict:
    """Load ruleset JSON from file"""
    ruleset_path = repo_root / RULESET_FILES.get(ruleset_type, ruleset_type)
    
    if not ruleset_path.exists():
        print(f"❌ Error: Ruleset file not found: {ruleset_path}")
        sys.exit(1)
    
    with open(ruleset_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_repo_info(repo: str) -> tuple[str, str]:
    """Parse owner/repo string"""
    if '/' not in repo:
        print(f"❌ Error: Repository must be in format OWNER/REPO, got: {repo}")
        sys.exit(1)
    
    owner, repo_name = repo.split('/', 1)
    return owner, repo_name


def list_existing_rulesets(owner: str, repo: str, token: str) -> list:
    """List existing rulesets in the repository"""
    if httpx is None:
        print("❌ Error: httpx is required for API calls. Install with: pip install httpx")
        sys.exit(1)
    
    url = f"https://api.github.com/repos/{owner}/{repo}/rulesets"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    try:
        response = httpx.get(url, headers=headers, timeout=30.0)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPError as e:
        print(f"❌ Error listing rulesets: {e}")
        return []


def apply_ruleset(owner: str, repo: str, ruleset_data: dict, token: str, dry_run: bool = False) -> bool:
    """Apply ruleset to repository via GitHub API"""
    if not dry_run and httpx is None:
        print("❌ Error: httpx is required for API calls. Install with: pip install httpx")
        print("   Or use --dry-run to test without making API calls")
        sys.exit(1)
    
    url = f"https://api.github.com/repos/{owner}/{repo}/rulesets"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    
    if dry_run:
        print("🔍 Dry run mode - would send the following ruleset:")
        print(json.dumps(ruleset_data, indent=2))
        return True
    
    try:
        response = httpx.post(url, headers=headers, json=ruleset_data, timeout=30.0)
        response.raise_for_status()
        result = response.json()
        print(f"✅ Ruleset created successfully!")
        print(f"   ID: {result.get('id')}")
        print(f"   Name: {result.get('name')}")
        return True
    except httpx.HTTPStatusError as e:
        print(f"❌ Error applying ruleset: {e}")
        print(f"   Status: {e.response.status_code}")
        print(f"   Response: {e.response.text}")
        return False
    except httpx.HTTPError as e:
        print(f"❌ Error applying ruleset: {e}")
        return False


def update_bypass_actors(ruleset_data: dict, team_ids: Optional[list] = None, 
                        integration_ids: Optional[list] = None) -> dict:
    """Update bypass actors in ruleset data"""
    bypass_actors = []
    
    # Add teams
    if team_ids:
        for team_id in team_ids:
            bypass_actors.append({
                "actor_id": team_id,
                "actor_type": "Team",
                "bypass_mode": "always"
            })
    
    # Add integrations/apps
    if integration_ids:
        for integration_id in integration_ids:
            bypass_actors.append({
                "actor_id": integration_id,
                "actor_type": "Integration",
                "bypass_mode": "always"
            })
    
    # Add repository role bypass (admin)
    bypass_actors.append({
        "actor_id": 1,  # Admin role
        "actor_type": "RepositoryRole",
        "bypass_mode": "always"
    })
    
    ruleset_data["bypass_actors"] = bypass_actors
    return ruleset_data


def main():
    parser = argparse.ArgumentParser(
        description="Apply GitHub tag ruleset to protect release tags",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run with standard ruleset
  python tools/apply_tag_ruleset.py --token ghp_xxx --repo TEC-The-ELidoras-Codex/TEC_Q5EP --dry-run

  # Apply standard ruleset
  python tools/apply_tag_ruleset.py --token ghp_xxx --repo TEC-The-ELidoras-Codex/TEC_Q5EP

  # Apply strict semantic versioning ruleset
  python tools/apply_tag_ruleset.py --token ghp_xxx --repo TEC-The-ELidoras-Codex/TEC_Q5EP --ruleset strict-semver

  # With bypass actors
  python tools/apply_tag_ruleset.py --token ghp_xxx --repo TEC-The-ELidoras-Codex/TEC_Q5EP --team-id 123456
        """
    )
    
    parser.add_argument(
        "--token",
        required=True,
        help="GitHub personal access token with repo admin permissions"
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="Repository in format OWNER/REPO"
    )
    parser.add_argument(
        "--ruleset",
        choices=list(RULESET_FILES.keys()),
        default="standard",
        help="Ruleset type to apply (default: standard)"
    )
    parser.add_argument(
        "--team-id",
        type=int,
        action="append",
        dest="team_ids",
        help="Team ID to add as bypass actor (can be specified multiple times)"
    )
    parser.add_argument(
        "--integration-id",
        type=int,
        action="append",
        dest="integration_ids",
        help="Integration/App ID to add as bypass actor (can be specified multiple times)"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List existing rulesets and exit"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be applied without making changes"
    )
    
    args = parser.parse_args()
    
    # Get repository root
    repo_root = Path(__file__).parent.parent
    
    # Parse repo info
    owner, repo_name = get_repo_info(args.repo)
    
    print(f"🎯 Target: {owner}/{repo_name}")
    print(f"📋 Ruleset: {args.ruleset}")
    print()
    
    # List existing rulesets if requested
    if args.list:
        print("📋 Listing existing rulesets...")
        rulesets = list_existing_rulesets(owner, repo_name, args.token)
        if rulesets:
            for ruleset in rulesets:
                print(f"  - {ruleset.get('name')} (ID: {ruleset.get('id')}, Target: {ruleset.get('target')})")
        else:
            print("  No rulesets found or error occurred")
        return 0
    
    # Load ruleset data
    print(f"📂 Loading ruleset from {RULESET_FILES[args.ruleset]}...")
    ruleset_data = load_ruleset(args.ruleset, repo_root)
    
    # Update bypass actors if specified
    if args.team_ids or args.integration_ids:
        print(f"👥 Adding bypass actors...")
        if args.team_ids:
            print(f"   Teams: {args.team_ids}")
        if args.integration_ids:
            print(f"   Integrations: {args.integration_ids}")
        ruleset_data = update_bypass_actors(ruleset_data, args.team_ids, args.integration_ids)
    
    # Apply ruleset
    print()
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        print()
    
    print(f"🚀 Applying ruleset '{ruleset_data['name']}'...")
    success = apply_ruleset(owner, repo_name, ruleset_data, args.token, args.dry_run)
    
    if success and not args.dry_run:
        print()
        print("✨ Success! Your release tags are now protected.")
        print()
        print("📖 Next steps:")
        print("   1. Go to repository Settings → Rules → Rulesets to review")
        print("   2. Test tag creation with: git tag -s v1.0.0-test")
        print("   3. Verify CI/CD checks are required before tag push")
        print()
        print("📚 Documentation: .github/TAG_RULESET_README.md")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
