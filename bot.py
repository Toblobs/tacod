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

        general_field = """
        `/help`
        > **Location**: Anywhere
        > **User Requirements**: None

        *This command that you are seeing right now.* 

        `/ping`
        > **Location**: Anywhere
        > **User Requirements**: Manage Guild

        *Pings the bot and returns a latency time in milliseconds.*
        """
        
        e.add_field(name = '__General Commands__', value = general_field, inline = False)
        
        captcha_field = """
        `/generate_new_led`
        > **Location**: Anywhere
        > **Arguments**: 
        > `num` for the LED #number that you want. If supplied as -1, generates a completely random LED.
        > `threshold` to supply a custom weight threshold that all generated indexes must be over to qualify as ON.
        > **User Requirements**: None

        *Generates a fresh LED display randomly based on internal weights.*

        `/captcha`
        > **Location**: DMs Only
        > **User Requirements**: None

        *Generates a TACOD Captcha. Respond by clicking one of the buttons assossiciated with an option.*

        `/userinfo`
        > **Location**: Anywhere
        > **User Requirements**: None
        > **Arguments**: `user` for the user (ignored unless used by @Toblobs)

        *Gives some information on your usage of TACOD. This is a tool you can use to request your data.*
        """

        e.add_field(name = '__Captcha Commands__', value = captcha_field, inline = False)

        e.set_footer(text = 'TACOD: A Synergy Studios Project')
        e.timestamp = datetime.now(timezone.utc)

        await context.response.send_message(embed = e)

    @commands.slash_command(description = 'Basic test ping command. Returns a delay in sending command measured in milliseconds.')
    @commands.default_member_permissions(manage_guild = True)
    async def ping(self, context):

        time_taken = (context.created_at - datetime.now(timezone.utc)).microseconds / 1000
        await context.response.send_message(f'**Pong**! 🏓\n`Responded in {time_taken} ms`')

class CaptchaCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(description = 'Generates a fresh LED display randomly based on internal weights.')
    async def generate_new_led(self, context: disnake.ApplicationCommandInteraction, num = -1, threshold = -1):

        if threshold == -1:
            threshold = await get_confidence_threshold()
        
        weights_array = np.random.uniform(low = LOW_RANDOM_WEIGHTS, high = HIGH_RANDOM_WEIGHTS, size = (LED_DIMENSIONS[0], LED_DIMENSIONS[1]))
      
        random_line_num = random.randint(3, 6)
        weights_array, lines = generate_lines(weights_array, random_line_num)

        random_led = generate_using_weights(weights_array, threshold = float(threshold))
        
        led_embed = disnake.Embed(title = f'__Generated LED__')
        led_embed.color = disnake.Colour.from_rgb(87, 230, 87)
        led_embed.timestamp = datetime.now(timezone.utc)

        led_embed.description = f'```\n{random_led.__str__()}\n```'

        led_embed.add_field(name = 'Weights Array', value = f'```python\n{weights_array.__str__()}\n```', inline = False)
        led_embed.add_field(name = 'LED Statistics', value = f"> - **Threshold**: {threshold}\n> - ON `⬜` LED cells: {len(random_led.get_on_coords())}\n> - OFF `⬛` LED cells: {len(random_led.get_off_coords())}\n> - **Lines Generated**: `📏`: {random_line_num} / `{lines}`", inline = False)
        led_embed.set_footer(text = 'TACOD: A Synergy Studios Project')

        await context.response.send_message(embed = led_embed)

    async def generate_captcha_question(self):

        # for now, just return a sample question
        question = await fetch_question(0)
        return question
    
    @commands.slash_command(description = 'Gives some information on your usage of TACOD.')
    async def userinfo(self, context: disnake.ApplicationCommandInteraction):

        await context.response.send_message('Coming soon!')

    @commands.slash_command(description = 'Generates a captcha question that you can answer via buttons.')
    @commands.default_member_permissions(0)
    async def captcha(self, context: disnake.ApplicationCommandInteraction):

        if context.guild:
            return

        question = await self.generate_captcha_question()

        question_embed = disnake.Embed(title = f'__Captcha Question__')
        question_embed.color = disnake.Colour.from_rgb(87, 230, 87)
        question_embed.timestamp = datetime.now(timezone.utc)

        question_embed.description = f'**Please answer**: {question.question}'
        view = disnake.ui.View()

        async def button_listener(btn_context: disnake.MessageInteraction):
            
            split = btn_context.component.custom_id.split(':')

            if split[0] == 'captcha':

                # Make and save Response object
                response = Response(await get_responses_length(), question.id, int(split[2]), context.author.id, datetime.now(timezone.utc))
                await save_response(response)

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