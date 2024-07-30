# bot.py // @toblobs

from __init__ import *

from led import *
from question import *

from dbio import *

from disnake.ext import commands

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = False

tacod_bot = commands.Bot(command_prefix = '/',  intents = disnake.Intents.all(), command_sync_flags = command_sync_flags)

class AdminCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 

    @commands.slash_command(description = 'Gives information about TACOD bot.')
    async def help(self, context):

        e = disnake.Embed(title = 'TACOD Help Page')
        e.color = disnake.Colour.from_rgb(230, 126, 34)

        e.description = """This page gives information on commands and an FAQ on the TACOD bot."""
        e.set_footer(text = 'TACOD: A Synergy Studios Project')

        await context.response.send_message(embed = e)

    @commands.slash_command(description = 'Basic test ping command. Returns a delay in sending command measured in milliseconds.')
    @commands.default_member_permissions(manage_guild = True)
    async def ping(self, context):

        time_taken = (context.created_at - datetime.now(timezone.utc)).microseconds / 1000
        await context.response.send_message(f'**Pong**! 🏓\n`Responded in {time_taken} ms`')

class CaptchaCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    def generate_captcha_question(self):

        # for now, just return a sample question
        question = fetch_question(0)
        return question
    
    @commands.slash_command(description = 'Generates a captcha question that you can answer via buttons, reactions or dropdown menus.')
    @commands.default_member_permissions(0)
    async def captcha(self, context: disnake.ApplicationCommandInteraction):

        if context.guild:
            return

        question = self.generate_captcha_question()

        question_embed = disnake.Embed(title = f'__Captcha Question__')
        question_embed.color = disnake.Colour.from_rgb(87, 230, 87)
        question_embed.timestamp = datetime.now(timezone.utc)

        question_embed.description = f'**Please answer**: {question.question}'
        view = disnake.ui.View()

        async def button_listener(btn_context: disnake.MessageInteraction):
            
            split = btn_context.component.custom_id.split(':')

            if split[0] == 'captcha':

                # Make and save Response object
                response = Response(get_responses_length(), question.id, int(split[2]), context.author.id, datetime.now(timezone.utc))
                save_response(response)

                # Save result answer in TACOD bot log channel
                channel = self.bot.get_channel(CHANNEL)
                await channel.send(f'**{context.author.mention} completed captcha ID `{question.id}` with response ID `{response.id}` > Option #{split[2]}.**', embed = question_embed)
                await btn_context.send(f'Response of Option #{split[2]} has been saved.')

        for led in question.leds:

            num = question.leds.index(led) + 1
        
            # Embed handling
            question_embed.add_field(name = f'Option #{num}', value = f'```\n{led.__str__()}\n```', inline = True)
            
            # Button handling
            new_button = disnake.ui.Button(label = f'{num}', style = disnake.ButtonStyle.primary, custom_id = f'captcha:button:{num}:{question.id}')
            new_button.callback = button_listener

            view.add_item(new_button)

        question_embed.set_footer(text = 'TACOD: A Synergy Studios Project')

        await context.response.send_message(embed = question_embed, view = view)

tacod_bot.add_cog(AdminCommands(tacod_bot))
tacod_bot.add_cog(CaptchaCommands(tacod_bot))