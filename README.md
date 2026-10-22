# Morning Briefing Agent

An agent that reads your unread Gmail, your upcoming Google Calendar events, and your recent Slack messages, then writes a short briefing with five sections:  URGENT, UPCOMING EVENTS, SLACK HIGHLIGHTS, OTHER EMAILS, and SUGGESTED ACTIONS.  I built it for Pursuit L2 (Cycle 2) with the Strands Agents SDK and Claude.

## Safety

- **Read-only.**  The three tools (`check_gmail`, `check_calendar`, `check_slack`) cannot send, reply, accept, edit, or delete anything.
- **Narrow access.**  The Google sign-in asks only for `gmail.readonly` and `calendar.readonly`.  The Slack token reads channels only; it cannot read direct messages.
- **Marketing filter.**  Code removes marketing email before the model sees it.
- **Untrusted input.**  The prompt tells the model to treat every email, event, and Slack message as data and never to follow instructions inside them.

## Try it on fake data

Fake mode needs no Google or Slack account, only a Claude API key.

1. Use Python 3.12.
2. Create a virtual environment and install the packages:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install strands-agents litellm python-dotenv google-api-python-client google-auth-oauthlib slack_sdk
   ```

3. Create a file named `.env` with one line:  `ANTHROPIC_API_KEY=your-key-here`
4. Optional key check:  `python test_model.py`
5. Run the agent:  `python agent.py --mock > run.txt`
6. Grade the briefing with the keyword checker:  `python grade_briefing.py run.txt`

The grader covers only the checks that keywords can judge.  Read the briefing yourself against `mock_expectations.md` for the rest, such as whether the agent obeyed the injection email in the fake inbox.

## Files

| File | Purpose |
|---|---|
| `agent.py` | The agent, its three tools, the system prompt, and the marketing filter |
| `mock_data.py` | Fake inbox, calendar, and Slack messages, including a prompt-injection email |
| `mock_expectations.md` | What a good briefing must do and must not do |
| `mock_results.md` | Graded results of every mock run |
| `grade_briefing.py` | Keyword grader for saved briefings |
| `run*.txt` | Saved output of each mock run |
| `test_model.py` | Checks that the Claude key works |
| `top_senders.py` | Lists your busiest sender domains, to help you fill `BLOCK_SENDERS` |

## Live use

1. Create a Google OAuth client (type "Desktop app"), save it as `credentials.json` in this folder, and run `python agent.py`.  The first run opens a browser to sign in and saves `token.json`.
2. Create a Slack app with the user scopes `channels:read`, `channels:history`, `groups:read`, and `groups:history`.  Put its user token in `.env` as `SLACK_BOT_TOKEN`.
3. Optional in `.env`:  `KEEP_SENDERS` (never filter these) and `BLOCK_SENDERS` (always filter these), each a comma-separated list; `MODEL_ID` to change the model.

Never commit `.env`, `token.json`, or `credentials.json`; `.gitignore` blocks all three.
