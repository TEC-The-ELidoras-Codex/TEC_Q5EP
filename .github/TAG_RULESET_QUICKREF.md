# Tag Ruleset Quick Reference

## 🎯 What Are These Files?

JSON configurations for GitHub tag rulesets that protect release tags in TEC_Q5EP.

## 📁 Files

| File | Purpose | Tags Protected |
|------|---------|----------------|
| `tag-ruleset-release-protection.json` | Standard protection | `v*`, `release-*` |
| `tag-ruleset-strict-semver.json` | Strict semantic versioning | `v*` only |

## 🛡️ Protection Features

Both rulesets enforce:
- ✅ **Restrict creation/update/deletion** - Prevent unauthorized changes
- ✅ **Require signed commits** - GPG signature verification
- ✅ **Require CI/CD checks** - All tests must pass
- ✅ **Block force pushes** - Immutable history
- ✅ **Conventional commits** - Structured commit messages
- ✅ **Valid author email** - Prevent spoofing

### Strict Semver Additional Rule
- ✅ **Enforce `vX.Y.Z` format** - Reject non-semantic version tags

## ⚡ Quick Apply

### Using Python Script (Recommended)
```bash
# Dry run to preview
python tools/apply_tag_ruleset.py \
  --token YOUR_GITHUB_TOKEN \
  --repo TEC-The-ELidoras-Codex/TEC_Q5EP \
  --dry-run

# Apply standard ruleset
python tools/apply_tag_ruleset.py \
  --token YOUR_GITHUB_TOKEN \
  --repo TEC-The-ELidoras-Codex/TEC_Q5EP

# Apply strict semver ruleset
python tools/apply_tag_ruleset.py \
  --token YOUR_GITHUB_TOKEN \
  --repo TEC-The-ELidoras-Codex/TEC_Q5EP \
  --ruleset strict-semver
```

### Using GitHub CLI
```bash
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /repos/TEC-The-ELidoras-Codex/TEC_Q5EP/rulesets \
  --input .github/tag-ruleset-release-protection.json
```

### Manual (GitHub Web UI)
1. Go to **Settings** → **Rules** → **Rulesets**
2. Click **New ruleset** → **New tag ruleset**
3. Copy the JSON content and import/configure manually

## 📚 Full Documentation

- **Detailed Guide**: [TAG_RULESET_README.md](TAG_RULESET_README.md)
- **Release Process**: [../docs/RELEASE_PROCESS.md](../docs/RELEASE_PROCESS.md)
- **Main README**: [../README.md](../README.md)

## 🔑 Required Status Checks

Tags can only be created when these CI/CD jobs pass:
- `test-python` - Python test suite
- `test-ui` - UI build and tests  
- `security-scan` - Trivy vulnerability scan

Defined in: [workflows/ci-cd.yml](workflows/ci-cd.yml)

## 🚀 Example Usage

After applying the ruleset, create a release:

```bash
# On main branch with all checks passing
git checkout main
git pull

# Create signed tag
git tag -s v1.2.0 -m "Release v1.2.0: New features"

# Push (will be validated against ruleset)
git push origin v1.2.0
```

If any ruleset rule fails, the tag push will be rejected.

## ❓ Troubleshooting

**"Tag creation blocked by ruleset"**
- Ensure all CI/CD checks passed
- Verify tag name format (`vX.Y.Z`)
- Sign your tag with GPG (`-s` flag)

**"httpx not found" in apply script**
```bash
pip install httpx
# or
pip install -r requirements.txt
```

**More help**
See [TAG_RULESET_README.md](TAG_RULESET_README.md#-troubleshooting)

---

**Build. Validate. Commit. Ship.** 🚀
