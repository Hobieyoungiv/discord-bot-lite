"""Everyday commands: /ping, /serverinfo, /userinfo, /poll, /help."""
from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from utils.helpers import color

NUMBER_EMOJI = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Check that the bot is alive and see its response time.")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)} ms")

    @app_commands.command(name="serverinfo", description="Show info about this server.")
    @app_commands.guild_only()
    async def serverinfo(self, interaction: discord.Interaction):
        g = interaction.guild
        e = discord.Embed(title=g.name, color=color(self.bot))
        if g.icon:
            e.set_thumbnail(url=g.icon.url)
        e.add_field(name="Members", value=str(g.member_count))
        e.add_field(name="Channels", value=str(len(g.channels)))
        e.add_field(name="Roles", value=str(len(g.roles)))
        e.add_field(name="Created", value=discord.utils.format_dt(g.created_at, "D"))
        if g.owner_id:
            e.add_field(name="Owner", value=f"<@{g.owner_id}>")
        await interaction.response.send_message(embed=e)

    @app_commands.command(name="userinfo", description="Show info about a member.")
    @app_commands.describe(member="Who to look up (leave empty for yourself)")
    @app_commands.guild_only()
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member | None = None):
        m = member or interaction.user
        e = discord.Embed(title=str(m), color=m.color if m.color.value else color(self.bot))
        e.set_thumbnail(url=m.display_avatar.url)
        e.add_field(name="Joined server", value=discord.utils.format_dt(m.joined_at, "R") if m.joined_at else "?")
        e.add_field(name="Account created", value=discord.utils.format_dt(m.created_at, "R"))
        roles = [r.mention for r in reversed(m.roles) if r != interaction.guild.default_role]
        e.add_field(name=f"Roles ({len(roles)})", value=" ".join(roles[:15]) or "None", inline=False)
        await interaction.response.send_message(embed=e)

    @app_commands.command(name="poll", description="Make a quick poll with up to 5 options.")
    @app_commands.describe(question="The question", options="Options separated by | (leave empty for a yes/no poll)")
    @app_commands.guild_only()
    async def poll(self, interaction: discord.Interaction, question: str, options: str | None = None):
        choices = [o.strip() for o in (options or "").split("|") if o.strip()]
        if len(choices) > 5:
            await interaction.response.send_message("Max 5 options.", ephemeral=True)
            return
        e = discord.Embed(title=f"📊 {question}", color=color(self.bot))
        e.set_footer(text=f"Poll by {interaction.user.display_name}")
        if choices:
            e.description = "\n".join(f"{NUMBER_EMOJI[i]} {c}" for i, c in enumerate(choices))
            emojis = NUMBER_EMOJI[: len(choices)]
        else:
            emojis = ["👍", "👎"]
        await interaction.response.send_message(embed=e)
        msg = await interaction.original_response()
        for emoji in emojis:
            await msg.add_reaction(emoji)

    @app_commands.command(name="help", description="List the bot's commands.")
    async def help(self, interaction: discord.Interaction):
        e = discord.Embed(title="Commands", color=color(self.bot))
        guild = discord.Object(id=self.bot.guild_id) if self.bot.guild_id else None
        for cmd in sorted(self.bot.tree.get_commands(guild=guild), key=lambda c: c.name):
            e.add_field(name=f"/{cmd.name}", value=cmd.description or "-", inline=False)
        await interaction.response.send_message(embed=e, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Utility(bot))
