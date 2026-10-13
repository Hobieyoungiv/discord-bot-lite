"""Welcome new members with a message and (optionally) give them a starting role.

Settings live in config.json: welcome_channel_id, welcome_message, auto_role_id.
"""
from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands

from utils.helpers import color


def render(template: str, member: discord.Member) -> str:
    return (template.replace("{mention}", member.mention)
                    .replace("{name}", member.display_name)
                    .replace("{server}", member.guild.name)
                    .replace("{count}", str(member.guild.member_count)))


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def build_embed(self, member: discord.Member) -> discord.Embed:
        template = self.bot.config.get("welcome_message") or "Welcome to {server}, {mention}!"
        e = discord.Embed(description=render(template, member), color=color(self.bot))
        e.set_author(name=f"Welcome, {member.display_name}!", icon_url=member.display_avatar.url)
        e.set_thumbnail(url=member.display_avatar.url)
        e.set_footer(text=f"Member #{member.guild.member_count}")
        return e

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        cfg = self.bot.config
        role_id = int(cfg.get("auto_role_id") or 0)
        if role_id and not member.bot:
            role = member.guild.get_role(role_id)
            if role:
                try:
                    await member.add_roles(role, reason="Auto-role on join")
                except discord.HTTPException:
                    self.bot.log.warning("Couldn't give auto-role %s. Is my role above it?", role_id)
        channel_id = int(cfg.get("welcome_channel_id") or 0)
        channel = member.guild.get_channel(channel_id) if channel_id else None
        if isinstance(channel, discord.TextChannel):
            try:
                await channel.send(content=member.mention, embed=self.build_embed(member))
            except discord.HTTPException:
                self.bot.log.warning("Couldn't post in welcome channel %s", channel_id)

    @app_commands.command(name="welcometest", description="Preview the welcome message using yourself.")
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.guild_only()
    async def welcometest(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=self.build_embed(interaction.user), ephemeral=True)


async def setup(bot):
    await bot.add_cog(Welcome(bot))
