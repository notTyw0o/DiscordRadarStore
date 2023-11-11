from discord.ext import commands, tasks
from discord.commands import Option
import mongo
import util_function
import client_data
import discordembed
import discord_menu as menu

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ctx = None
        self.last_message = None

    @commands.slash_command(
        description='Check if bot is ready to use!',
    )
    async def check(self, ctx):
        request = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if request.get('status') == 200 and isAuthor.get('status') == 200:
            msg = request.get('message')
            await ctx.respond(f'{msg}')
        elif isAuthor.get('status') == 400:
            msg = isAuthor.get('message')
            await ctx.respond(f'{msg}')
        elif request.get('status') == 400:
            await ctx.respond(request.get('message'))

    @commands.slash_command(
        name='addproduct',
        description='Add new product to database!',
    )
    async def addproduct(
        self, 
        ctx, 
        productname: Option(str, 'Name of the product!', required=True),
        productid: Option(str, 'ID of the product!', required=True),
        productprice: Option(int, 'Set price of the product!', required=True),
        roleid: Option(str, 'Set price of the product!', required=True)
        ):
        request = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if request.get('status') == 200 and isAuthor.get('status') == 200:
            productRequest = await mongo.addProduct(productname, productid, productprice, roleid)
            await ctx.respond(f'{productRequest}')
        elif request.get('status') != 200:
            await ctx.respond(request.get('message'))
        elif isAuthor.get('status') != 200:
            msg = isAuthor.get('message')
            await ctx.respond(f'{msg}')

    @commands.slash_command(
    name='removeproduct',
    description='Remove product by its ID',
    )
    async def removeproduct(
        self, 
        ctx, 
        productid: Option(str, 'ID of the product!', required=True),
        ):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            result = await mongo.removeproduct(productid)
            await ctx.respond(f'{result}')
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='addassets',
    description='Add template assets to databases!',
    )
    async def addassets(
        self, 
        ctx, 
        ):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            result = await mongo.addtemplate()
            await ctx.respond(f'{result}')
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='changeassets',
    description='Change template assets in databases!',
    )
    async def changeassets(
        self, 
        ctx,
        assetsid: Option(str, 'Target assets ID!', required=True),
        value: Option(str, 'Value of assets ID!', required=True),
        ):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            result = await mongo.changeassets(assetsid, value)
            await ctx.respond(f'{result}')
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='showassets',
    description='Show template assets in databases!',
    )
    async def showassets(
        self, 
        ctx,
        ):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        result = await mongo.showassets()
        template = await mongo.getassets();
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200 and result.get('status') == 200:
            try:
                footer = {'name': ctx.author.name,'time': await util_function.timenow(), 'avatar': ctx.author.avatar.url}
            except:
                footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
            await ctx.respond(embed= await discordembed.showembed(result.get('assets'), template.get('assets'), footer))
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        elif result.get('status') == 400:
            await ctx.respond(result.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='setprice',
    description='Set a new price for the product!',
    )
    async def setprice(
        self, 
        ctx,
        productid: Option(str, 'Target product ID!', required=True),
        productprice: Option(int, 'Set a new price for the product!', required=True),
        ):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            request = await mongo.setprice(productid, productprice)
            await ctx.respond(f'{request}')
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='addstock',
    description='Add stock to the databases!',
    )
    async def addstock(
        self, 
        ctx,
        productid: Option(str, 'Target product ID!', required=True),
        productdetails: Option(str, 'Details of the product!', required=True),
        ):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            request = await mongo.addstock(productid, productdetails)
            await ctx.respond(f'{request}')
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='addstockbulk',
    description='Add stock to the databases!',
    )
    async def addstockbulk(
        self, 
        ctx,
        productid: Option(str, 'Target product ID!', required=True),
        productdetails: Option(str, 'Details of the product!', required=True),
        ):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            request = await mongo.addstockbulk(productid, productdetails)
            await ctx.respond(f'{request}')
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='showstock',
    description='Show stock from the databases!',
    )
    async def showstock(
        self, 
        ctx,
        productid: Option(str, 'Target product ID!', required=True),
        ):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            request = await mongo.showstock(productid)
            await ctx.respond("**Product ID: " + productid + "**" + "\n" + "```\n" + request + "\n```")
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='removestock',
    description='Remove stock from the databases!',
    )
    async def removestock(
        self, 
        ctx,
        productid: Option(str, 'Target product ID!', required=True),
        index: Option(int, 'Select which index you want to remove!', required=False)
        ):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            if index is None:
                isAll = True
            else:
                isAll = False
            request = await mongo.removestock(productid, index, isAll)
            await ctx.respond(f'{request}')
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='send',
    description='Send product to user!',
    )
    async def send(
        self, 
        ctx,
        discordid: Option(str, 'Discord ID of the target!', required=True),
        productid: Option(str, 'Target product ID!', required=True),
        amount: Option(int, 'How many product u want to send!', required=True)
        ):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            try:
                user = ctx.guild.get_member(int(discordid))
            except:
                user = 'error'
            if user == 'error' or user is None:
                await ctx.respond(f'User not found!')
            else:
                request = await mongo.takestock(productid, amount)
                if request.get('status') == 200:
                    await user.send(request.get('message'))
                    await ctx.respond('Check DM' + "'" + 's!')
                else:
                    await ctx.respond(request.get('message'))
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='deploy',
    description='Deploy user command!',
    )
    async def deploy(self, ctx):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            try:
                footer = {'name': ctx.author.name,'time': await util_function.timenow(), 'avatar': ctx.author.avatar.url}
            except:
                footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
            embed = await discordembed.deploy(footer)
            await ctx.respond('Success!', ephemeral=True)
            await ctx.send(embed=embed, view=menu.MainView(timeout=None))
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='give',
    description='Give balance to user ID!',
    )
    async def give(self, ctx, discordid: Option(str, 'Discord ID of the target!', required=True), type: Option(str, '"worldlock" or "rupiah"!', required=True), amount: Option(int, 'Amount balance!', required=True)):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            request = await mongo.give(discordid, type, amount)
            await ctx.respond(f'{request}')
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='setwebhook',
    description='Set webhook url!',
    )
    async def setwebhook(self, ctx, webhookurl: Option(str, 'Discord Webhook URL!', required=True)):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            request = await mongo.setwebhook(webhookurl)
            await ctx.respond(f'{request}')
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='setdeposit',
    description='Set deposit info!',
    )
    async def setdeposit(self, ctx, world: Option(str, 'Input deposit world!', required=True), owner: Option(str, 'The owner of the world!', required=True)):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            request = await mongo.setdeposit(world, owner)
            await ctx.respond(f'{request}')
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='setorderstate',
    description='Set deposit info!',
    )
    async def setorderstate(self, ctx, state: Option(str, 'True or False', required=True)):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            if state in ['True', 'False']:
                request = await mongo.setorderstate(state)
                await ctx.respond(f'{request}')
            else:
                await ctx.respond(f'Wrong state typing!')
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='setpresence',
    description='Set deposit info!',
    )
    async def setpresence(self, ctx, presence: Option(str, 'Your new presence!', required=True)):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            request = await mongo.setpresence(presence)
            await ctx.respond(request)
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='setchannelhistory',
    description='Set channel history info!',
    )
    async def setchannelhistory(self, ctx, channelid: Option(str, 'Your new presence!', required=True)):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            request = await mongo.setchannelhistory(channelid)
            await ctx.respond(request)
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @tasks.loop(seconds=5.0)
    async def runlivestock(self, ctx):
        if self.last_message:  # If there's a previous message
            request = await mongo.checkstock()
            template = await mongo.getassets()
            if request.get('status') == 200 and template.get('status') == 200:
                try:
                    footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': ctx.author.avatar.url}
                except:
                    footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                embed = await discordembed.checkstockembed(request, template.get('assets'), footer)
                await self.last_message.delete()  # Delete the previous message
                self.last_message = await ctx.send(embed=embed)
        else:
            request = await mongo.checkstock()
            template = await mongo.getassets()
            if request.get('status') == 200 and template.get('status') == 200:
                try:
                    footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': ctx.author.avatar.url}
                except:
                    footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                embed = await discordembed.checkstockembed(request, template.get('assets'), footer)
                self.last_message = await ctx.send(embed=embed)

    @commands.slash_command(
    name='startlivestock',
    description='Start livestock info!',
    )
    async def startlivestock(self, ctx):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            self.ctx = ctx
            self.runlivestock.start(ctx)
            await ctx.respond('Livestock deployed!', ephemeral=True)
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='stoplivestock',
    description='Stop livestock info!',
    )
    async def stoplivestock(self, ctx):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            self.runlivestock.cancel()
            await ctx.respond('Livestock stopped!', ephemeral=True)
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='showlogs',
    description='Show logs info!',
    )
    async def showlogs(self, ctx):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            request = await mongo.showlogs()
            message = ''
            for data in request['data']:
                product = data['product'].rstrip('\n')
                message += f"===============================\nDiscord ID: {data['discordid']}\nProduct Name: {data['productname']}\nAmount: {data['amount']}\nTotal Price: {data['totalprice']}\nProduct: \n{product}" + '\n'
            message += f"==============================="
            await ctx.respond(f"```{message}```", ephemeral=True)
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))

    @commands.slash_command(
    name='deletelogs',
    description='Delete logs info!',
    )
    async def deletelogs(self, ctx):
        isOwner = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if isOwner.get('status') == 200 and isAuthor.get('status') == 200:
            request = await mongo.deletelogs()
            await ctx.respond(request['message'], ephemeral=True)
        elif isAuthor.get('status') == 400:
            await ctx.respond(isAuthor.get('message'))
        else:
            await ctx.respond(isOwner.get('message'))
        

def setup(bot):
    bot.add_cog(Commands(bot))