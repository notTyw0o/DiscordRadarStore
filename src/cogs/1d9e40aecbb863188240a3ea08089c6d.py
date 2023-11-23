from discord.ext import commands, tasks
from discord.commands import Option
import mongo
import util_function
import client_data
import discordembed
import discord_menu as menu
import hotmailbox

class CommandsCustom1d9e40aecbb863188240a3ea08089c6d(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx = None
        self.last_message = None

    @commands.slash_command(
    name='hotmailbalance',
    description='Check hotmail balance!',
    )
    async def hotmailbalance(self, ctx):
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isAuthor.get('status') == 200:
            request = await hotmailbox.getbalance()
            if request['status'] == 200:
                embed = await discordembed.textembed(f"Balance : {request['data']['BalanceUsd']} USD")
            else:
                embed = await discordembed.textembed(request['message'])
            await ctx.respond(embed=embed)
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
    
    @tasks.loop(seconds=5.0)
    async def runlivestockemail(self, ctx, template):
        if self.last_message:  # If there's a previous message
            request = await hotmailbox.getstockemail()
            template = template
            if request.get('status') == 200 and template.get('status') == 200:
                try:
                    footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': ctx.author.avatar.url}
                except:
                    footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                
                embed = await discordembed.checkstockembed(request, template.get('assets'), footer)
                
                # Check if the last message is still valid
                try:
                    last_message = await ctx.fetch_message(self.last_message.id)
                except:
                    last_message = None
                
                if last_message:
                    await last_message.edit(embed=embed, view=menu.MainViewEmail(timeout=None))
                else:
                    self.last_message = await ctx.send(embed=embed, view=menu.MainViewEmail(timeout=None))
        else:
            request = await hotmailbox.getstockemail()
            template = await mongo.getassets()
            if request.get('status') == 200 and template.get('status') == 200:
                try:
                    footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': ctx.author.avatar.url}
                except:
                    footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                embed = await discordembed.checkstockembed(request, template.get('assets'), footer)
                self.last_message = await ctx.send(embed=embed, view=menu.MainViewEmail(timeout=None))

    @commands.slash_command(
    name='deployemail',
    description='Deploy livestock and menu!',
    )
    async def deploy(self, ctx):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            self.ctx = ctx
            self.runlivestockemail.start(ctx, await mongo.getassets())
            await ctx.respond('Livestock deployed!', ephemeral=True)
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='stopdeployemail',
    description='Stop deploy info!',
    )
    async def stopdeployemail(self, ctx):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            self.runlivestockemail.cancel()
            await ctx.respond('Livestock stopped!', ephemeral=True)
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

def setup(bot):
    bot.add_cog(CommandsCustom1d9e40aecbb863188240a3ea08089c6d(bot))