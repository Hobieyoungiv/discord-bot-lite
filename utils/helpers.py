"""Shared helpers."""
from __future__ import annotations

import discord


def color(bot) -> discord.Color:
    try:
        return discord.Color(int(str(bot.config.get("embed_color", "5865F2")).lstrip("#"), 16))
    except ValueError:
        return discord.Color.blurple()
