# bot.py // @toblobs

from __init__ import *

from disnake.ext import commands

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = False

tacod_bot = commands.Bot(command_prefix = '/', description = 'TACOD Bot', help_command = None, intents = disnake.Intents.all(), command_sync_flags = command_sync_flags)

class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 

    @commands.slash_command(description = 'Gives information about TACOD bot.')
    async def help(self, context):

        help_str = f"""```fix
TACOD Bot Help Page 
«⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯»

This command gives some information on commands and on how to use TACOD bot.

ADMIN COMMANDS

/help
Brings up this help page.

/ping [Required Permissions: Manage Server]
Basic test ping command. Returns a delay in sending command measured in milliseconds.


CAPTCHA COMMANDS

/captcha [Required Location: Direct Messages Only]
Generates a captcha question that you can answer via buttons, reactions or dropdown menus.
Only usable in Direct Messages with the TACOD bot.

... (to be added)

```
                    """
        await context.response.send_message(help_str)

    @commands.slash_command(description = 'Basic test ping command. Returns a delay in sending command measured in milliseconds.')
    @commands.default_member_permissions(manage_guild = True)
    async def ping(self, context):

        time_taken = (context.created_at - datetime.now(timezone.utc)).microseconds / 1000
        await context.response.send_message(f'**Pong**! 🏓\n`Responded in {time_taken} ms`')

class CaptchaCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description = 'Generates a captcha question that you can answer via buttons, reactions or dropdown menus.')
    @commands.default_member_permissions(0)
    async def captcha(self, context):

        if context.guild:
            return

        await context.response.send_message(f'[Insert CAPTCHA question here.]')
        



tacod_bot.add_cog(AdminCommands(tacod_bot))
tacod_bot.add_cog(CaptchaCommands(tacod_bot))
