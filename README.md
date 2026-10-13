# Discord Bot Lite (discord.py starter template)

A free, clean, ready-to-run Discord bot template in Python (discord.py 2.x) with slash commands. Clone it, paste your token, and run it.

**Included in this free version:**

| Feature | Commands |
|---|---|
| Welcome messages + auto-role for new members | `/welcometest` |
| Utility | `/ping` `/serverinfo` `/userinfo` `/poll` `/help` |

- Modern slash commands, so members just type `/`.
- Instant command sync to your server while you develop (set `GUILD_ID`).
- Settings in one file (`config.json`), and a cog layout that's easy to extend.

---

## Want moderation, levels and self-roles too?

The full **[Discord Bot Starter Kit](https://hobieyoung.gumroad.com/l/discord-bot-starter-kit)** adds everything most servers want, on the same code base:

| | Lite (free) | Full kit |
|---|:---:|:---:|
| Welcome messages + auto-role | Yes | Yes |
| `/ping` `/serverinfo` `/userinfo` `/poll` `/help` | Yes | Yes |
| Moderation with a log channel: `/kick` `/ban` `/timeout` `/purge` `/warn` `/warnings` | | Yes |
| XP levels, `/rank`, `/leaderboard`, level-up reward roles | | Yes |
| Button self-roles that survive restarts (`/rolemenu`) | | Yes |
| Built-in SQLite database (nothing to install) | | Yes |
| Paste-your-token window, no file editing | | Yes |
| Template cog for adding your own commands | | Yes |

**[Get the full kit here](https://hobieyoung.gumroad.com/l/discord-bot-starter-kit)**

**Need a custom bot built for your server?** I build them to order: **[Fiverr: custom Discord bot](https://www.fiverr.com/hobieyoungiv)**

---

## Setup (about 10 minutes)

### Step 1: Install Python
Download Python 3.10 or newer from [python.org/downloads](https://www.python.org/downloads/).
**On Windows, tick "Add python.exe to PATH"** on the first installer screen.

### Step 2: Create your bot on Discord
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and click **New Application**.
2. Open the **Bot** tab:
   - Click **Reset Token**, then **Copy**. This is your bot's password. Keep it secret.
   - Under **Privileged Gateway Intents**, turn on **Server Members Intent** (needed for welcome messages) and click **Save**.
3. Open **OAuth2**, then **URL Generator**:
   - Scopes: **bot** and **applications.commands**.
   - Bot permissions: **Manage Roles, Send Messages, Embed Links, Add Reactions, Read Message History, View Channels**.
   - Open the URL at the bottom and add the bot to your server.

### Step 3: Add your token
Rename `.env.example` to `.env`, open it, and paste your token after `DISCORD_TOKEN=`.
Optional: put your server ID after `GUILD_ID=` so commands appear instantly.

### Step 4: Run it
- **Windows:** double-click `start.bat`.
- **Mac/Linux:** run `sh start.sh`.

The first run installs everything automatically. Type `/help` in your server to see the commands.

## Settings (`config.json`)

| Setting | What it does |
|---|---|
| `status_text` | The bot's "Playing ..." status |
| `embed_color` | Hex color for the bot's messages |
| `welcome_channel_id` | Channel for welcome messages (0 = off) |
| `welcome_message` | Text with `{mention}` `{name}` `{server}` `{count}` |
| `auto_role_id` | Role given to new members (0 = off) |

To get an ID: Discord Settings > Advanced > turn on Developer Mode, then right-click a channel or role and click **Copy ID**.

## Adding your own commands
Add a file in `cogs/`, copy the structure of `cogs/utility.py`, and add its name to `COGS` in `bot.py`.

## License
MIT. Use it for anything.
