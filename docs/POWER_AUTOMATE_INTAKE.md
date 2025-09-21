# Power Automate: Email Intake Flow

Goal: capture email + attachments arriving to `intake@elidorascodex.com` and archive them into SharePoint `TEC-Operations/Intake`. No code, just clicks.

## Prereqs

- Shared mailbox `intake@elidorascodex.com` (or an alias pointing to your licensed mailbox)
- SharePoint site: TEC-Operations
- Document library: Intake
- Optional: SharePoint list IntakeIndex with columns Source, Topic, Tags, ImportedBy, OriginalSender, WhenReceived

## Steps (click-by-click)

1) Go to make.powerautomate.com → Create → Automated cloud flow
2) Name: TEC Intake; Trigger: When a new email arrives in a shared mailbox (V2)
3) Shared mailbox address: `intake@elidorascodex.com`
4) New step: Initialize variable ‘folderPath’ = concat('/TEC-Operations/Intake/Inbox/', utcNow('yyyy'), '/', utcNow('MM'), '/')
5) Action: Create file (SharePoint)
   - Site address: TEC-Operations
   - Folder path: use folderPath
   - File name: concat(triggerOutputs()?['body/subject'], '_', ticks(utcNow()), '.eml')
   - File content: Original mail (dynamic content)
6) Condition: Has Attachments equals true
   - If yes → Apply to each: Attachments → Create file (SharePoint)
     - Site: TEC-Operations
     - Folder path: /TEC-Operations/Intake/Attachments/@{utcNow('yyyy')}/@{utcNow('MM')}/
     - File name: Attachments Name
     - File content: Attachments Content
7) Optional: Create item (SharePoint) in IntakeIndex
   - Fields: Source (Choice), Topic (Subject), Tags (parse from subject or leave blank), ImportedBy (user), OriginalSender (From), WhenReceived (Received time)
8) Optional: Send an email (V2) to the original sender confirming receipt with a link to the created file
9) Save and test: send a message to `intake@` and confirm files and list item appear

## Tips

- Use a separate “External Uploads” folder with Request files enabled for non-tenant contributors; then have a second flow to sweep new files into Intake.
- Add a retention label to Intake after you decide on your record-keeping policy.
