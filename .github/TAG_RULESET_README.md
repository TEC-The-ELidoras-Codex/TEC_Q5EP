# GitHub Tag Ruleset for Release Protection

This directory contains JSON configurations for GitHub tag rulesets that protect release tags and enforce security and workflow hygiene.

## 🎯 Overview

We provide two ruleset configurations:

1. **`tag-ruleset-release-protection.json`** - Standard release protection for `v*` and `release-*` tags
2. **`tag-ruleset-strict-semver.json`** - Strict semantic versioning enforcement for `v*` tags only

## 🛡️ Standard Release Protection Ruleset

**File:** `tag-ruleset-release-protection.json`

### Target Tags
Applies to tags matching:
- `v*` (e.g., `v1.0.0`, `v2.1.3`, `v1.0.0-alpha`)
- `release-*` (e.g., `release-alpha`, `release-final`, `release-staging`)

### Rules Enabled

| Rule | Purpose |
|------|---------|
| ✅ **Restrict tag creation** | Only authorized users can create release tags |
| ✅ **Restrict tag updates** | Prevent modification of existing tags |
| ✅ **Restrict tag deletion** | Prevent unauthorized tag removal |
| ✅ **Require signed commits** | Ensure cryptographic authenticity via GPG signatures |
| ✅ **Require status checks to pass** | Enforce CI/CD success before tagging (`test-python`, `test-ui`, `security-scan`) |
| ✅ **Block force pushes (non-fast-forward)** | Preserve tag history integrity |
| ✅ **Conventional Commits pattern** | Enforce structured commit messages |
| ✅ **Valid author email** | Prevent spoofing of author info |

### Required Status Checks
- `test-python` - Python test suite must pass
- `test-ui` - UI build and tests must pass
- `security-scan` - Security vulnerability scan must pass

## 🔒 Strict Semantic Versioning Ruleset

**File:** `tag-ruleset-strict-semver.json`

### Target Tags
Applies only to tags matching: `v*`

### Additional Rules
In addition to all standard rules, this ruleset enforces:

| Rule | Purpose |
|------|---------|
| ✅ **Semantic Versioning 2.0.0 format** | Tags must match `vX.Y.Z` or `vX.Y.Z-prerelease+build` format |

**Valid Examples:**
- `v1.0.0`
- `v2.1.3`
- `v1.0.0-alpha`
- `v1.0.0-alpha.1`
- `v1.0.0-rc.1+build.123`

**Invalid Examples:**
- `v1` (missing minor/patch)
- `v1.2` (missing patch)
- `v01.0.0` (leading zeros)
- `release-alpha` (doesn't match pattern)

### Regex Pattern
```regex
^v(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$
```

## 📋 How to Apply These Rulesets

### Option 1: GitHub Web UI

1. Go to your repository **Settings** → **Rules** → **Rulesets**
2. Click **New ruleset** → **New tag ruleset**
3. Copy the JSON content from either configuration file
4. Click **Import a ruleset** (if available) or manually configure:
   - Set **Ruleset name** (e.g., `release-protection`)
   - Set **Enforcement status** to **Active**
   - Under **Target tags**, add:
     - `refs/tags/v*`
     - `refs/tags/release-*` (if using standard ruleset)
   - Enable the rules listed in the JSON
5. Configure **Bypass actors** (optional):
   - Add `@your-org/release-admins` team
   - Add any release automation bots
6. Click **Create** or **Save changes**

### Option 2: GitHub CLI

```bash
# Install GitHub CLI if not already installed
# https://cli.github.com/

# Apply the ruleset using the API
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /repos/OWNER/REPO/rulesets \
  --input .github/tag-ruleset-release-protection.json
```

### Option 3: GitHub REST API

```bash
# Using curl with personal access token
curl -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.github.com/repos/OWNER/REPO/rulesets \
  -d @.github/tag-ruleset-release-protection.json
```

### Option 4: Python Script (Automated)

See the included `tools/apply_tag_ruleset.py` script for automated application.

## 🔧 Customization

### Adding Bypass Actors

To allow specific users, teams, or apps to bypass the rules:

```json
"bypass_actors": [
  {
    "actor_id": 1,
    "actor_type": "Team",
    "bypass_mode": "always"
  },
  {
    "actor_id": 2,
    "actor_type": "RepositoryRole",
    "bypass_mode": "pull_request"
  }
]
```

**Actor Types:**
- `Team` - GitHub team (requires team ID)
- `RepositoryRole` - Repository role (e.g., admin, maintain, write)
- `Integration` - GitHub App or integration

**Bypass Modes:**
- `always` - Can always bypass
- `pull_request` - Can bypass via pull request

### Getting Team/Integration IDs

```bash
# Get team ID
gh api /orgs/YOUR_ORG/teams/TEAM_NAME --jq .id

# Get integration ID
gh api /repos/OWNER/REPO/installations --jq '.[].id'
```

### Modifying Required Status Checks

Edit the `required_status_checks` array to match your CI/CD workflow:

```json
"required_status_checks": [
  {
    "context": "your-check-name",
    "integration_id": null
  }
]
```

Check names must match the job names in your `.github/workflows/*.yml` files.

## 🎭 Integration with CI/CD

Our `.github/workflows/ci-cd.yml` defines the following checks that are referenced in the rulesets:

- **test-python** - Runs Python test suite with pytest
- **test-ui** - Builds and tests the UI components
- **security-scan** - Runs Trivy vulnerability scanner

Tags can only be created when all these checks pass.

## 🚀 Release Workflow Example

Once the ruleset is applied, your release workflow becomes:

1. **Develop and test** your changes on a feature branch
2. **Open a PR** to `main` branch
3. **CI/CD runs automatically** (test-python, test-ui, security-scan)
4. **Review and merge** the PR once all checks pass
5. **Create a tag** from the merged commit:
   ```bash
   git checkout main
   git pull
   git tag -s v1.2.0 -m "Release v1.2.0: New features"
   git push origin v1.2.0
   ```
6. **GitHub validates** the tag against the ruleset rules
7. **Tag is created** if all rules pass (or rejected if not)

### Using GitHub Actions for Automated Tagging

See the included workflow example: `.github/workflows/release.yml`

## 🔐 Security Best Practices

1. **Enable commit signing**
   ```bash
   # Configure GPG signing
   git config --global commit.gpgsign true
   git config --global user.signingkey YOUR_KEY_ID
   ```

2. **Protect the main branch**
   - Require pull request reviews
   - Require status checks to pass
   - Require signed commits

3. **Limit tag creation permissions**
   - Only allow maintainers or release team to create tags
   - Use bypass actors sparingly

4. **Audit tag creation**
   - Review repository audit logs regularly
   - Set up notifications for tag events

## 📚 References

- [GitHub Rulesets Documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GPG Commit Signing](https://docs.github.com/en/authentication/managing-commit-signature-verification)

## 🛠️ Troubleshooting

### "Tag creation blocked by ruleset"
- Ensure all required status checks have passed
- Verify the tag name matches the expected pattern
- Check that your commit is signed (if required)
- Verify you have permission to create tags

### "Status check not found"
- Ensure the check name matches exactly (case-sensitive)
- Wait for all CI/CD jobs to complete
- Check that the CI/CD workflow ran successfully

### "Invalid tag name format"
- For strict semver ruleset: use `vX.Y.Z` format
- Avoid leading zeros: `v1.0.0` not `v01.0.0`
- Pre-release tags: `v1.0.0-alpha.1`
- Build metadata: `v1.0.0+build.123`

---

**Build. Validate. Commit. Ship.** 🚀

For questions or issues, see the main [README.md](/README.md) or open an issue.
