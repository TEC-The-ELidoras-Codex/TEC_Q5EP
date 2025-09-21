# TEC IT Runbook (Foundations)

This is your one-pager to stand up TEC’s collaboration and mail, migrate personal data safely, and lay a minimal Azure baseline. Follow in order; check boxes as you go.

## 0) Identities and mail

- One licensed mailbox: <KaznakAlpha@elidorascodex.com>
- Keep root admin only for admin: <kaznakalpha@elidorascodex.onmicrosoft.com> (Bitwarden)
- Everything else is an alias or shared mailbox (no extra license)
  - Aliases examples: Privacy@, Gheddz@, KilljoyKaznak@ → all land in KaznakAlpha inbox
  - Shared mailbox: intake@ (for automated capture) or family@ (for group mail)

Checklist

- [ ] Admin Center → Users → Active users → Select KaznakAlpha → Manage email aliases → add the aliases
- [ ] Shared mailbox → Create ‘intake@’ → add yourself as Member and grant ‘Send as’

## 1) DNS: mail deliverability

Required now

- [ ] MX @ → elidorascodex-com.mail.protection.outlook.com (priority 0, TTL 3600)
- [ ] CNAME autodiscover → autodiscover.outlook.com
- [ ] TXT (SPF) @ → v=spf1 include:spf.protection.outlook.com -all
- [ ] Remove Zoho/Titan MX + extra SPF records (only one SPF allowed)

Recommended next

- [ ] Enable DKIM in M365 → add the two CNAMEs the portal gives you (selector1/selector2)
- [ ] Keep DMARC TXT: _dmarc → v=DMARC1; p=none; (later move to quarantine/reject)

## 2) Migration: email history

Goal: move historic mail from Zoho/Outlook.com/Gmail → Exchange Online.

Options

- [ ] Exchange Admin Center → Migration → IMAP (Zoho/Gmail). Use app passwords if needed.
- [ ] Outlook desktop: add both accounts, drag folders, or Export .PST then Import.
- [ ] Export MBOX (Zoho/Gmail) → convert/import via Outlook

During cutover

- [ ] Set forwarding at legacy providers to intake@ or KaznakAlpha@ (keep copy until verified)
- [ ] When done, cancel legacy paid email (Titan/Zoho) and remove their DNS records

## 3) SharePoint/Teams: opinionated structure

Sites (keep it simple)

- TEC-Operations (policies, IT, legal)
  - Libraries: Runbooks, Legal-Privacy, Intake
- TEC-Codex (lore, research, creative)
  - Libraries: Published, Drafts, Archive

Checklist

- [ ] Create both sites and libraries
- [ ] Create ‘Intake’ library list columns: Source, Topic, Tags, ImportedBy, OriginalSender, WhenReceived
- [ ] Teams: one team ‘TEC-Core’ with channels: ops, codex, announcements

## 4) Automation: Intake flow (no code)

Use Power Automate to capture email into SharePoint automatically.

- [ ] Trigger: When a new email arrives (shared mailbox intake@)
- [ ] Actions:
  - Create file (.eml) in /TEC-Operations/Intake/Inbox/yyyy/MM/
  - Save attachments in /TEC-Operations/Intake/Attachments/yyyy/MM/
  - Create list item with Source, OriginalSender, WhenReceived, Topic, Tags
- [ ] Optional: auto-reply to sender with a receipt and URL to the item

See ‘docs/POWER_AUTOMATE_INTAKE.md’ for a click-by-click guide.

## 5) Copilot Search: Acronyms + Bookmarks

- [ ] Acronyms: in Copilot Search → Acronyms, add one entry → Export template CSV → fill 25 rows → Import → Publish
- [ ] Bookmarks: add 5–10 pointing to your ‘Published’ SharePoint pages (DMARC, DKIM, KAZNAK, Entropic Protocol, Privacy Inbox)

Starter CSV: ‘docs/acronyms_template.csv’ (adjust to match exported headers).

## 6) Files migration (fast)

- [ ] Install OneDrive personal and OneDrive for work; sign into both; drag folders from personal → TEC-Codex/Drafts
- [ ] Use SharePoint Migration Tool (SPMT) for Google Drive or large shares → TEC-Codex/Drafts
- [ ] Promote finished documents from Drafts → Published

## 7) Azure baseline (minimal)

This sets a safe foundation for future deployment and artifacts. Run from your machine with Azure CLI.

Resources

- Resource Group: rg-tec-core (eastus)
- Storage Account: sttectecore (Standard_LRS, no public blob access)
- Key Vault: kv-tec-core (soft delete + purge protection)
- App Service Plan: asp-tec-core (Linux B1)
- Web App: app-tec-q5ep (Python 3.13), app settings WEBSITES_PORT=8000, SCM_DO_BUILD_DURING_DEPLOYMENT=true

CLI (paste one-by-one in PowerShell)

- Set subscription
  - az account set -s 89d36e9a-a518-4151-95b3-087ec1b88ec5
- Create RG
  - az group create --name rg-tec-core --location eastus
- Storage
  - az storage account create --name sttectecore --resource-group rg-tec-core --location eastus --sku Standard_LRS --allow-blob-public-access false
- Key Vault
  - az keyvault create --name kv-tec-core --resource-group rg-tec-core --location eastus --enable-purge-protection --enable-soft-delete
- App Service Plan
  - az appservice plan create --name asp-tec-core --resource-group rg-tec-core --location eastus --sku B1 --is-linux
- Web App
  - az webapp create --name app-tec-q5ep --resource-group rg-tec-core --plan asp-tec-core --runtime PYTHON:3.13
- App settings
  - az webapp config appsettings set --name app-tec-q5ep --resource-group rg-tec-core --settings WEBSITES_PORT=8000 SCM_DO_BUILD_DURING_DEPLOYMENT=true

Notes

- Don’t deploy yet if you’re not ready; this just reserves names and gives you a vault and storage for artifacts.
- When you deploy, use a startup command like ‘uvicorn server.app:app --host 0.0.0.0 --port 8000’. We can wire this later.

## 8) Security quick hits

- [ ] MFA enforced for admin and primary user
- [ ] DKIM on; DMARC p=none → quarantine after a week
- [ ] Limit ChatGPT/enterprise apps to admins or small groups via Entra ID → Enterprise apps → Permissions

## 9) Weekly rhythm

- Publish a weekly ‘TEC Updates’ (Viva Engage): what moved, what published, what’s next
- Review Acronyms/Bookmarks for drift
- Archive Drafts older than 60 days unless active

---

If you want to expand any section into automation (Python/Graph, SPMT, PowerShell), we can modularize this into small scripts later.

***End of Runbook***
