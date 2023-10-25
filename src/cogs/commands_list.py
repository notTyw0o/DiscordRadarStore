from discord.ext import commands
from discord.commands import Option
import mongo
import util_function
import client_data

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='add',
        description='Add two numbers',
    )
    async def add(self, ctx, first: Option(int, 'The first number', required=True), second: Option(int, 'The second number', required=True)):
        result = first + second
        await ctx.respond(f'The sum of {first} and {second} is {result}')

    @commands.slash_command(
        description='Check if bot is ready to use!',
    )
    async def check(self, ctx):
        request = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if request.get('status') != 0 and isAuthor.get('status') == 200:
            msg = request.get('message')
            await ctx.respond(f'{msg}')
        elif isAuthor.get('status') != 200:
            msg = isAuthor.get('message')
            await ctx.respond(f'{msg}')
        else:
            await ctx.respond(f'Internal server error!')

    @commands.slash_command(
        name='addproduct',
        description='Add new product to database!',
    )
    async def addproduct(
        self, 
        ctx, 
        productname: Option(str, 'Name of the product!', required=True),
        productid: Option(str, 'ID of the product!', required=True),
        productprice: Option(int, 'Set price of the product!', required=True)
        ):
        request = await mongo.checkOwner(client_data.SECRET_KEY)
        isAuthor = await util_function.isAuthor(ctx.author.id, client_data.OWNER_ID)
        if request.get('status') == 200 and isAuthor.get('status') == 200:
            productRequest = await mongo.addProduct(productname, productid, productprice)
            await ctx.respond(f'{productRequest}')
        elif request.get('status') != 200:
            await ctx.respond(f'Bot is not active!')
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
            await ctx.respond(f'Internal server error!')

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
            await ctx.respond(f'Internal server error!')

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
            await ctx.respond(f'Internal server error!')

    @commands.slash_command(
    name='showstock',
    description='Add stock to the databases!',
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
            await ctx.respond(f'Internal server error!')

    @commands.slash_command(
    name='removestock',
    description='Add stock to the databases!',
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
            await ctx.respond(f'Internal server error!')

def setup(bot):
    bot.add_cog(Commands(bot))
