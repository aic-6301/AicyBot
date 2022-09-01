import discord
from sembed import SAuthor, SEmbed, SField
from discord.ext import commands, components, syntaxer
import asyncio
import sentry_sdk
import sys
import os


class Cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name="on_command_error")
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.CommandNotFound):
            return
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            synt = syntaxer.Syntax(
                ctx.command,
                get_txt(ctx.guild.id, "help_detail")[str(ctx.command)],
            )
            e = discord.Embed(
                title=get_txt(ctx.guild.id, "missing_argument").format(
                    discord.utils.get(synt.args, param=error.param).name
                ),
                description=get_txt(ctx.guild.id, "missing_argument_desc").format(synt),
                color=Error,
            )
            return await components.reply(
                ctx.message,
                embed=e,
                components=[
                    components.Button(
                        get_txt(ctx.guild.id, "online_help"),
                        style=5,
                        url="https://sevenbot.jp/commands#" + str(ctx.command).replace(" ", "-"),
                    )
                ],
            )
        elif isinstance(error, discord.ext.BadArgument):
            e = discord.Embed(
                title=get_txt(ctx.guild.id, "bad_arg"),
                description=get_txt(ctx.guild.id, "see_help") + f"\n```\n{error}```",
                color=Error,
            )
            e.add_field(name="ヒント", value="[]、<>は不必要です。")

            return await components.reply(
                ctx,
                embed=e,
                components=[
                    components.Button(
                        "パラメータについてのヘルプ",
                        style=components.ButtonType.link,
                        url="https://sevenbot.jp/tutorial/command-howto",
                    )
                ],
            )
        elif isinstance(error, commands.MissingPermissions):
            res = ""
            for p in error.missing_permissions:
                try:
                    res += get_txt(ctx.guild.id, "permissions_text")[0][p] + "\n"
                except KeyError:
                    try:
                        res += get_txt(ctx.guild.id, "permissions_text")[1][p] + "\n"
                    except KeyError:
                        res += get_txt(ctx.guild.id, "permissions_text")[2][p] + "\n"
            e = discord.Embed(
                title=get_txt(ctx.guild.id, "missing_permissions")[0],
                description=get_txt(ctx.guild.id, "missing_permissions")[1] + f"```\n{res}```",
                color=Error,
            )
            return await ctx.reply(embed=e)
        elif isinstance(error, commands.errors.NotOwner):
            e = discord.Embed(title=get_txt(ctx.guild.id, "only_admin"), color=Error)
            return await ctx.reply(embed=e)
        elif isinstance(error, commands.errors.CommandOnCooldown):
            e = discord.Embed(
                title=get_txt(ctx.guild.id, "cooldown"),
                description=get_txt(ctx.guild.id, "cooldown_desc").format(round(error.retry_after, 2)),
                color=Error,
            )
            return await ctx.reply(embed=e)
        elif isinstance(error, commands.errors.DisabledCommand):
            e = discord.Embed(title=get_txt(ctx.guild.id, "disabled"), color=Error)
            return await ctx.reply(embed=e)
        elif isinstance(error, commands.errors.NSFWChannelRequired):
            e = discord.Embed(title="このコマンドはNSFWチャンネル限定です。", color=Error)
            return await ctx.reply(embed=e)
        else:
            sentry_sdk.capture_exception(error)
            e = discord.Embed(
                title="エラーが発生しました。",
                description=f"```\n{error}```",
                color=discord.Colour.red,
            )
            msg = await ctx.reply(embed=e)
            await msg.add_reaction(self.bot.oemojis["down"])
            try:
                error_msg = "".join(traceback.TracebackException.from_exception(error).format())
                await bot.wait_for(
                    "reaction_add",
                    check=lambda reaction, user: (not isinstance(reaction.emoji, str))
                    and reaction.emoji.name == "down"
                    and reaction.message.id == msg.id
                    and reaction.count == 2,
                )
                e = discord.Embed(
                    title=get_txt(ctx.guild.id, "error"),
                    description=f"```\n{error_msg[-1990:]}```",
                    color=Error,
                )
                await msg.edit(embed=e)
            except asyncio.TimeoutError:
                pass
            return
        
    @commands.Cog.listener()
    async def on_command_suggest(self, ctx: commands.Context, suggested_commands):
        e = SEmbed(
            title="不明なコマンドです。",
            description="`a!help`で確認してください。",
            color=discord.Colour.Red,
        )
        suggested_commands = filter(
            lambda x: set(x) & set(ctx.message.content.split(" ")[0].removeprefix(ctx.prefix)), suggested_commands
        )
        if not suggested_commands:
            e.fields.append(
                SField(
                    name="もしかして：",
                    value="見付かりませんでした。",
                    inline=False,
                )
            )
        else:
            e.fields.append(
                SField(
                    name="もしかして：",
                    value="```\n",
                    inline=False,
                )
            )
            for s in suggested_commands:
                bv = e.fields[0].value
                e.fields[0].value += s + "\n"
                if len(e.fields[0].value) > 250:
                    e.fields[0].value = bv
                    break
            e.fields[0].value += "```"
            await ctx.reply(embed=e)

async def setup(bot):
    await bot.add_cog(Cogs(bot))
