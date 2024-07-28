# bot.py // @toblobs

from __init__ import *
from led import *

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

        self.questions = []

    def generate_captcha_question(self):

        # for now, just return a sample question
        one = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 0, 0]]))

        two = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 1, 0, 0, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 0, 0, 0, 0]]))

        three = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 0, 0, 0, 0]]))
        
        four = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                       [0, 1, 0, 1, 0],
                                       [0, 1, 0, 1, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 0, 0]]))

        five = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 1, 0, 0, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 0, 0, 0, 0]]))

        six = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 1, 0, 0, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 1, 0, 1, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 0, 0, 0, 0]]))

        seven = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 1, 0],
                                       [0, 0, 0, 0, 0]]))
        
        eight = create_display_from_ids(np.matrix([[0, 0, 0, 0, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 1, 0, 1, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 1, 0, 1, 0],
                                       [0, 1, 1, 1, 0],
                                       [0, 0, 0, 0, 0]]))

        return Question('Which display looks the most like a **7**?', 0, [one, two, three, four, five, six, seven, eight], 6)

    @commands.slash_command(description = 'Generates a captcha question that you can answer via buttons, reactions or dropdown menus.')
    @commands.default_member_permissions(0)
    async def captcha(self, context: disnake.ApplicationCommandInteraction):

        if context.guild:
            return

        question = self.generate_captcha_question()
        self.questions.append(question)

        question_embed = disnake.Embed(title = f'__Captcha Question__')
        question_embed.color = disnake.Colour.from_rgb(87, 230, 87)
        question_embed.timestamp = datetime.now(timezone.utc)

        question_embed.description = f'**Please answer**: {question.question}'
        view = disnake.ui.View()

        async def button_listener(btn_context: disnake.MessageInteraction):
            
            split = btn_context.component.custom_id.split(':')

            if split[0] == 'captcha':

                if split[2] == 'submit':
                    pass

                else:
                    btn_context.component.disabled = True

            await btn_context.send(f'You pressed button {split[2]}')
            await context.edit_original_message(view = view)
            
        for led in question.leds:

            num = question.leds.index(led) + 1

            question_embed.add_field(name = f'Option #{num}', value = f'```\n{led.__str__()}\n```', inline = True)
            
            new_button = disnake.ui.Button(label = f'{num}', style = disnake.ButtonStyle.primary, custom_id = f'captcha:button:{num}:{question.id}')
            new_button.callback = button_listener

            view.add_item(new_button)

        submit_button = disnake.ui.Button(label = 'Submit', style = disnake.ButtonStyle.green, custom_id = f'captcha:button:submit')
        submit_button.callback = button_listener

        view.add_item(submit_button)

        question_embed.set_footer(text = 'TACOD: A Synergy Studios Project')

        await context.response.send_message(embed = question_embed, view = view)

tacod_bot.add_cog(AdminCommands(tacod_bot))
tacod_bot.add_cog(CaptchaCommands(tacod_bot))