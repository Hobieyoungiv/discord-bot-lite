"""Discord Bot Lite - main entry point.

Run with:  python bot.py   (or double-click start.bat on Windows)
"""
from __future__ import annotations

import json
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parent
COGS = ["cogs.utility", "cogs.welcome"]


def setup_logging() -> logging.Logger:
    (ROOT / "logs").mkdir(exist_ok=True)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    file_handler = RotatingFileHandler(ROOT / "logs" / "bot.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    file_handler.setFormatter(fmt)
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [file_handler, console]
    return logging.getLogger("bot")


def load_config() -> dict:
    with open(ROOT / "config.json", encoding="utf-8") as f:
        return json.load(f)


discord.VoiceClient.warn_nacl = False  # this kit doesn't use voice, so skip the voice-library warnings
if hasattr(discord.VoiceClient, "warn_dave"):
    discord.VoiceClient.warn_dave = False


class StarterBot(commands.Bot):
    def __init__(self, config: dict, guild_id: int | None = None):
        intents = discord.Intents.default()
        intents.members = True          # needed for welcome messages + auto-role
        super().__init__(command_prefix=commands.when_mentioned, intents=intents, help_command=None)
        self.config = config
        self.guild_id = guild_id
        self.log = logging.getLogger("bot")

    async def setup_hook(self) -> None:
        for ext in COGS:
            await self.load_extension(ext)
            self.log.info("Loaded %s", ext)
        if self.guild_id:
            # Syncing to one server is instant; global sync can take up to an hour to show.
            guild = discord.Object(id=self.guild_id)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            self.log.info("Synced %d commands to server %s", len(synced), self.guild_id)
            # Remove any global copies from earlier runs so commands don't show up twice.
            self.tree.clear_commands(guild=None)
            await self.tree.sync()
        else:
            synced = await self.tree.sync()
            self.log.info("Synced %d commands globally (can take up to 1 hour to appear)", len(synced))

    async def on_ready(self) -> None:
        self.log.info("Logged in as %s (id %s) in %d server(s)", self.user, self.user.id, len(self.guilds))
        for g in self.guilds:
            self.log.info("  Server: %s (ID %s)", g.name, g.id)
        if not self.guilds:
            self.log.info("Not in any server yet. Invite it with the link from README step 2.")
        status = self.config.get("status_text")
        if status:
            await self.change_presence(activity=discord.Game(name=status))

def main() -> None:
    log = setup_logging()
    load_dotenv(ROOT / ".env")
    token = os.getenv("DISCORD_TOKEN", "").strip()
    if not token or token == "paste-your-token-here":
        log.error("No bot token found. Copy .env.example to .env and paste your token (see README.md, step 3).")
        raise SystemExit(1)
    guild = os.getenv("GUILD_ID", "").strip()
    bot = StarterBot(load_config(), int(guild) if guild.isdigit() else None)
    try:
        bot.run(token, log_handler=None)
    except discord.LoginFailure:
        log.error("Discord rejected the token. Copy a fresh one from the Developer Portal (Bot tab > Reset Token) into .env.")
        raise SystemExit(1)
    except discord.PrivilegedIntentsRequired:
        log.error("Turn on 'Server Members Intent' in the Developer Portal (Bot tab), then start the bot again.")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
