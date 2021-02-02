from discord.ext import commands
from helpers import programmes_helper
from services import ranks_service


class ClearrankCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clearrank(self, ctx, programme: str, year: int):
        user = ctx.message.author

        if programme is None:
            raise commands.UserInputError

        if programme == 'all':
            programme = None

        async with self.bot.db_conn.acquire() as connection:
            ranks = ranks_service.RanksService(connection)

            try:
                await ranks.delete_rank(str(user.id), programme, year)
            except ValueError:
                raise commands.UserInputError

        await ctx.send(user.mention + ' Rank cleared.')

    @clearrank.error
    async def info_error(self, ctx, error):
        user = ctx.message.author
        if isinstance(error, commands.UserInputError):
            await ctx.send(
                user.mention + f' Invalid arguments. Usage: '
                               f'`.clearrank <all/{programmes_helper.get_ids_string()}> <year>`')
        else:
            await ctx.send(user.mention + ' An unexpected error occurred')
            raise


def setup(bot):
    bot.add_cog(ClearrankCommand(bot))
