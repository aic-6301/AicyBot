from discord.ext import commands


def is_admin(self, user_id=None):
    def check(ctx):
        if isinstance(user_id, int):
            return user_id in self.bot.config["admins"]
        else:
            return ctx.author.id in self.bot.config["admins"]
    if user_id is None:
        return commands.check(check)
    else:
        return check(user_id)