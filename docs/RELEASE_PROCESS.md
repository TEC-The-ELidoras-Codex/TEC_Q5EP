# Release Process Guide

This guide explains how to create releases in TEC_Q5EP with tag protection enabled.

## 🎯 Overview

Our repository uses **GitHub tag rulesets** to protect release tags and ensure:
- All CI/CD checks pass before tagging
- Tags follow semantic versioning
- Commits are properly signed (recommended)
- Release history is immutable

## 📋 Release Checklist

Before creating a release:

- [ ] All changes are merged to `main` branch
- [ ] CI/CD pipeline passes (test-python, test-ui, security-scan)
- [ ] CHANGELOG updated (if applicable)
- [ ] Version number decided (following [Semantic Versioning](https://semver.org/))
- [ ] GPG signing configured (recommended)

## 🚀 Creating a Release

### Option 1: Manual Tag Creation (Recommended)

1. **Ensure you're on the latest main branch:**
   ```bash
   git checkout main
   git pull origin main
   ```

2. **Verify CI checks passed:**
   - Check GitHub Actions tab
   - Ensure test-python, test-ui, and security-scan are green

3. **Create a signed tag:**
   ```bash
   # For a stable release
   git tag -s v1.2.0 -m "Release v1.2.0: New features and bug fixes"
   
   # For a pre-release
   git tag -s v1.3.0-alpha.1 -m "Pre-release v1.3.0-alpha.1"
   ```
   
   **Note:** The `-s` flag signs the tag with your GPG key. If you don't have GPG configured, omit the `-s` flag, but be aware that unsigned tags may be rejected by stricter rulesets.

4. **Push the tag:**
   ```bash
   git push origin v1.2.0
   ```

5. **Create GitHub Release** (optional but recommended):
   - Go to repository → Releases → Draft a new release
   - Select your tag
   - Add release notes
   - Mark as pre-release if applicable
   - Publish release

### Option 2: Automated Release Workflow

Use the automated workflow for consistent releases:

1. **Go to Actions tab** → "Automated Release Tagging"
2. **Click "Run workflow"**
3. **Enter version** (e.g., `1.2.0` or `1.3.0-alpha.1`)
4. **Select pre-release status** if applicable
5. **Run workflow**

The workflow will:
- ✅ Validate version format
- ✅ Wait for all CI checks to pass
- ✅ Create a signed tag (if GPG configured)
- ✅ Push the tag
- ✅ Create a GitHub release with auto-generated notes

### Option 3: Using GitHub CLI

```bash
# Create and push tag
gh release create v1.2.0 \
  --title "Release v1.2.0" \
  --notes "Release notes here" \
  --verify-tag

# For pre-release
gh release create v1.3.0-alpha.1 \
  --title "Pre-release v1.3.0-alpha.1" \
  --notes "Alpha release notes" \
  --prerelease \
  --verify-tag
```

## 📝 Version Number Guidelines

Follow [Semantic Versioning 2.0.0](https://semver.org/):

### Format: `vMAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**Examples:**
- `v1.0.0` - First stable release
- `v1.1.0` - New features, backward compatible
- `v1.1.1` - Bug fixes only
- `v2.0.0` - Breaking changes
- `v2.0.0-alpha.1` - Pre-release alpha
- `v2.0.0-beta.2` - Pre-release beta
- `v2.0.0-rc.1` - Release candidate
- `v1.0.0+build.123` - Build metadata

### When to increment:

- **MAJOR** (X.0.0): Breaking changes, incompatible API changes
- **MINOR** (0.X.0): New features, backward compatible
- **PATCH** (0.0.X): Bug fixes, backward compatible

### Pre-release identifiers:

- `alpha` - Early development, unstable
- `beta` - Feature complete, testing phase
- `rc` - Release candidate, potentially stable

## 🔐 Setting Up GPG Signing

GPG signing ensures cryptographic verification of your releases.

### 1. Generate GPG Key (if you don't have one)

```bash
gpg --full-generate-key
# Choose RSA and RSA, 4096 bits
# Enter your name and email (must match your GitHub email)
```

### 2. List Your Keys

```bash
gpg --list-secret-keys --keyid-format=long
```

Output:
```
sec   rsa4096/YOUR_KEY_ID 2024-01-01 [SC]
uid   Your Name <your.email@example.com>
```

### 3. Export Your Public Key

```bash
gpg --armor --export YOUR_KEY_ID
```

Copy the output (including `-----BEGIN PGP PUBLIC KEY BLOCK-----` and end marker).

### 4. Add Key to GitHub

1. Go to GitHub → Settings → SSH and GPG keys
2. Click "New GPG key"
3. Paste your public key
4. Click "Add GPG key"

### 5. Configure Git to Sign Commits and Tags

```bash
git config --global user.signingkey YOUR_KEY_ID
git config --global commit.gpgsign true
git config --global tag.gpgsign true
```

### 6. Configure GPG for GitHub Actions (Optional)

For the automated workflow to sign tags:

1. Export your private key:
   ```bash
   gpg --armor --export-secret-keys YOUR_KEY_ID
   ```

2. Add to GitHub Secrets:
   - Go to repository → Settings → Secrets and variables → Actions
   - Add secret `GPG_PRIVATE_KEY` with your private key
   - Add secret `GPG_PASSPHRASE` with your key's passphrase

## 🛡️ Tag Ruleset Rules

Our repository enforces these rules for tags matching `v*` and `release-*`:

| Rule | Description |
|------|-------------|
| ✅ Creation restricted | Only authorized users can create tags |
| ✅ Update restricted | Tags cannot be modified once created |
| ✅ Deletion restricted | Tags cannot be deleted |
| ✅ Signed commits | Commits must be GPG signed (recommended) |
| ✅ Status checks | All CI/CD checks must pass |
| ✅ No force push | Tag history is immutable |
| ✅ Conventional commits | Commit messages must follow convention |
| ✅ Valid author email | Email must be properly formatted |

### Strict Semantic Versioning (Optional)

If the strict ruleset is enabled, tag names must exactly match:
```
v(MAJOR).(MINOR).(PATCH)[-prerelease][+build]
```

## 🚨 Troubleshooting

### "Tag creation was blocked by a ruleset"

**Cause:** One or more ruleset rules failed.

**Solutions:**
1. **Check CI status:** Ensure all checks passed on the commit
2. **Verify tag format:** Use `vX.Y.Z` format (e.g., `v1.2.0`)
3. **Sign your tag:** Use `git tag -s` instead of `git tag`
4. **Check permissions:** You may not have permission to create tags

### "Required status check 'test-python' has not passed"

**Cause:** CI/CD checks haven't completed or failed.

**Solutions:**
1. Wait for all checks to complete
2. Fix any failing tests
3. Ensure the commit you're tagging is in `main` branch where CI runs

### "GPG signature verification failed"

**Cause:** Your GPG key isn't properly configured.

**Solutions:**
1. Add your GPG public key to GitHub (see setup section)
2. Verify your git email matches your GPG key email
3. Ensure your key isn't expired: `gpg --list-keys`

### "Tag already exists"

**Cause:** The version tag already exists.

**Solutions:**
1. Choose a different version number
2. View existing tags: `git tag -l`
3. Delete local tag if needed: `git tag -d v1.2.0`

## 📚 Additional Resources

- [Semantic Versioning Specification](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [GitHub GPG Signing Guide](https://docs.github.com/en/authentication/managing-commit-signature-verification)
- [Tag Ruleset Documentation](.github/TAG_RULESET_README.md)

## 🎭 Release Workflow Summary

```
┌─────────────────────────────────────────────────────────────┐
│  1. Develop feature → PR → Review → Merge to main          │
├─────────────────────────────────────────────────────────────┤
│  2. CI/CD runs automatically (tests, builds, security)      │
├─────────────────────────────────────────────────────────────┤
│  3. All checks pass ✅                                       │
├─────────────────────────────────────────────────────────────┤
│  4. Decide version number (semantic versioning)             │
├─────────────────────────────────────────────────────────────┤
│  5. Create signed tag: git tag -s vX.Y.Z -m "Release..."   │
├─────────────────────────────────────────────────────────────┤
│  6. Push tag: git push origin vX.Y.Z                        │
├─────────────────────────────────────────────────────────────┤
│  7. GitHub validates against ruleset                        │
├─────────────────────────────────────────────────────────────┤
│  8. Tag created ✅ (or rejected if rules fail ❌)            │
├─────────────────────────────────────────────────────────────┤
│  9. Create GitHub Release (auto or manual)                  │
├─────────────────────────────────────────────────────────────┤
│  10. Deploy to production (optional, via CI/CD)             │
└─────────────────────────────────────────────────────────────┘
```

---

**Build. Validate. Commit. Ship.** 🚀

For questions, see the main [README.md](/README.md) or open an issue.
