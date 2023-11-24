import util_function

async def create_footer(ctx):
    try:
        footer = {'name': ctx.author.name,'time': await util_function.timenow(), 'avatar': ctx.author.avatar.url}
    except:
        footer = {'name': ctx.author.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
    return footer