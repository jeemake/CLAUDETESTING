# WhatsApp Draft Replies — n8n Workflow

An n8n workflow that automatically drafts replies to incoming WhatsApp messages using Claude AI.

## How It Works

```
Incoming WhatsApp Message
        │
        ▼
  Webhook Trigger (POST)
        │
        ▼
  Filter (has messages?)
     ┌──┴──┐
     No    Yes
     │      │
  200 OK   Extract message details
            │
            ▼
      Claude AI generates draft reply
            │
            ▼
      Format draft response
       ┌────┴────┐
       │         │
  Mark as Read  (Send Draft — disabled by default)
       │
       ▼
  Return draft via webhook response
```

## Nodes

| Node | Purpose |
|---|---|
| **WhatsApp Webhook Trigger** | Receives incoming messages via POST from WhatsApp Cloud API |
| **WhatsApp Verification (GET)** | Handles the webhook verification handshake |
| **Filter Incoming Messages** | Skips status updates and non-message events |
| **Extract Message Details** | Parses sender name, phone, and message text |
| **Generate Draft Reply (Claude)** | Calls the Anthropic API to draft a reply |
| **Format Draft Response** | Combines original message + draft into a clean object |
| **Mark Message as Read** | Sends a read receipt back to WhatsApp |
| **Send Draft to Self** | *(Disabled)* Optionally sends the draft back as a WhatsApp message |
| **Respond With Draft** | Returns the draft in the webhook HTTP response |

## Setup

### 1. Prerequisites

- An [n8n](https://n8n.io) instance (self-hosted or cloud)
- A [Meta WhatsApp Business API](https://developers.facebook.com/docs/whatsapp/cloud-api) account
- An [Anthropic API key](https://console.anthropic.com/)

### 2. Environment Variables

Set these in your n8n instance (Settings → Environment Variables):

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `WHATSAPP_ACCESS_TOKEN` | Permanent token from Meta Business |
| `WHATSAPP_VERIFY_TOKEN` | A secret string you choose for webhook verification |

### 3. Import the Workflow

1. Open your n8n instance
2. Go to **Workflows → Import from File**
3. Select `whatsapp-draft-replies.json`
4. Activate the workflow

### 4. Configure the WhatsApp Webhook

1. Copy your n8n webhook URL (shown in the Webhook Trigger node, e.g. `https://your-n8n.example.com/webhook/whatsapp-webhook`)
2. In the [Meta Developer Portal](https://developers.facebook.com/):
   - Go to your App → WhatsApp → Configuration
   - Set **Callback URL** to your webhook URL
   - Set **Verify Token** to the value of `WHATSAPP_VERIFY_TOKEN`
   - Subscribe to the `messages` field

### 5. Optional: Auto-Send Drafts

The **Send Draft to Self** node is disabled by default. To have the workflow send the drafted reply back as an actual WhatsApp message:

1. Open the workflow in the n8n editor
2. Click on the **Send Draft to Self** node
3. Enable it (toggle the "Disabled" switch off)

> **Warning**: Enabling auto-send means replies are sent without human review.

## Customization

### Change the AI Model

Edit the **Generate Draft Reply (Claude)** node and change the `model` field in the JSON body. Options include `claude-sonnet-4-20250514`, `claude-haiku-4-5-20251001`, etc.

### Modify the System Prompt

In the same node, update the `system` field to change how drafts are written. For example, you could instruct it to always reply in a specific language or tone.

### Store Drafts Instead of Responding

Replace the **Respond With Draft** node with a database node (e.g., PostgreSQL, Google Sheets, Airtable) to save drafts for later review.
