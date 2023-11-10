from discord.ext import commands, tasks
from discord.commands import Option
import mongo
import util_function
import client_data
import discordembed
import discord_menu as menu

class CommandsAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx = None
        self.last_message = None

    @commands.slash_command(
    name='deploylicense',
    description='Deploy user command!',
    )
    async def deploylicense(self, ctx):
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isAuthor.get('status') == 200:
            try:
                footer = {'name': ctx.author.name,'time': await util_function.timenow(), 'avatar': ctx.author.avatar.url}
            except:
                footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
            await ctx.respond('Success!', ephemeral=True)
            embed = await discordembed.deploylicense(footer)
            await ctx.send(embed=embed, view=menu.License(timeout=None))
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))

    @commands.slash_command(
    name='deploycontroller',
    description='Deploy user command!',
    )
    async def deploycontroller(self, ctx):
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isAuthor.get('status') == 200:
            try:
                footer = {'name': ctx.author.name,'time': await util_function.timenow(), 'avatar': ctx.author.avatar.url}
            except:
                footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
            await ctx.respond('Success!', ephemeral=True)
            embed = await discordembed.deploylicense(footer)
            await ctx.send(embed=embed, view=menu.Controller(timeout=None))
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))

    @commands.slash_command(
    name='deploydeposit',
    description='Deploy user command!',
    )
    async def deploydeposit(self, ctx):
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isAuthor.get('status') == 200:
            try:
                footer = {'name': ctx.author.name,'time': await util_function.timenow(), 'avatar': ctx.author.avatar.url}
            except:
                footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
            await ctx.respond('Success!', ephemeral=True)
            embed = await discordembed.deploylicense(footer)
            await ctx.send(embed=embed, view=menu.Deposit(timeout=None))
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))

    @commands.slash_command(
    name='deploygrowtopia',
    description='Deploy user command!',
    )
    async def deploygrowtopia(self, ctx):
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isAuthor.get('status') == 200:
            try:
                footer = {'name': ctx.author.name,'time': await util_function.timenow(), 'avatar': ctx.author.avatar.url}
            except:
                footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
            await ctx.respond('Success!', ephemeral=True)
            embed = await discordembed.deploylicense(footer)
            await ctx.send(embed=embed, view=menu.GrowtopiaStuff(timeout=None))
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))

    @commands.slash_command(
    name='addproductlisen',
    description='Add license product!',
    )
    async def addproductlisen(self, ctx, productprice: Option(int, 'Price of the product!', required=True), roleid: Option(str, 'Role ID!', required=True)):
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isAuthor.get('status') == 200:
            request = await mongo.addProductLisen(productprice, roleid)
            await ctx.respond(request)
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
            
    @commands.slash_command(
    name='addstocklisen',
    description='Add stock lisen product!',
    )
    async def addstocklisen(self, ctx, amount: Option(int, 'Price of the product!', required=True)):
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isAuthor.get('status') == 200:
            request = await mongo.addstocklisen(amount)
            await ctx.respond(request)
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))

def setup(bot):
    bot.add_cog(CommandsAdmin(bot))
