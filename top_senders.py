"""Show which sender domains fill your unread mail, to help you build BLOCK_SENDERS.

Usage:  python top_senders.py                    (looks back 30 days)
        python top_senders.py 7                  (looks back 7 days)
        python top_senders.py 30 gmail.com       (lists the top addresses inside one domain)

Runs on your Mac only.  It prints sender domains and counts to this terminal.
Nothing goes to the model, and no email text is read.
"""

import collections
import sys
import time
from email.utils import parseaddr

from googleapiclient.discovery import build

import agent

days = int(sys.argv[1]) if len(sys.argv) > 1 else 30
only_domain = sys.argv[2].lower() if len(sys.argv) > 2 else None
service = build("gmail", "v1", credentials=agent.get_google_credentials())
since = int(time.time()) - days * 86400

refs, token = [], None
while len(refs) < 300:
    page = service.users().messages().list(
        userId="me", q=f"is:unread after:{since}", maxResults=100, pageToken=token
    ).execute()
    refs += page.get("messages", [])
    token = page.get("nextPageToken")
    if not token:
        break

domains = collections.Counter()
for ref in refs[:300]:
    message = service.users().messages().get(
        userId="me", id=ref["id"], format="metadata", metadataHeaders=["From"]
    ).execute()
    sender = next((h["value"] for h in message["payload"]["headers"] if h["name"] == "From"), "")
    address = parseaddr(sender)[1].lower()
    domain = address.split("@")[-1] or "(unknown)"
    if only_domain:
        if domain == only_domain:
            domains[address] += 1
    else:
        domains[domain] += 1

scope = f" from {only_domain}" if only_domain else ""
print(f"Unread in the last {days} days{scope}: {sum(domains.values()) if only_domain else len(refs)} (counted up to 300)\n")
for domain, count in domains.most_common(15):
    print(f"{count:4}  {domain}")
print("\nTo filter a domain, add it to BLOCK_SENDERS in .env, separated by commas.")
print("To protect a sender, add it to KEEP_SENDERS.  Keep-list always wins.")
