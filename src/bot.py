import discord
from discord.ext import commands
import client_data
import mongo
import discordembed
import discord_function
import util_function
import mongo
import re

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

if client_data.SECRET_KEY == 'fc8af3e8ecf73bbd83597682037925d7':
    bot.load_extension('cogs.commands_admin')
    bot.load_extension('cogs.commands_user')
else:
    bot.load_extension('cogs.commands_user')
    try:
        bot.load_extension(f'cogs.{client_data.SECRET_KEY}')
    except:
        pass

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=client_data.PRESENCE))
    print(f'Logged in as {bot.user.name}')
    try:
        guildid = await mongo.getmuterole()
        guildid = guildid['guild']
        guild = bot.get_guild(int(guildid))

        if guild:
            await discord_function.fetch_mute_timers(guild)
    except:
        pass

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    invalid_prefixes = ['.', ',', '!', '>', '/']

    # Check if the message starts with any of the invalid prefixes
    if message.content.startswith(tuple(invalid_prefixes)):
        assets = await mongo.getassets()
        arrow = assets['assets']['sticker_1']
        embed = await discordembed.textembed('Command error, please use (/) slash commands!')
        await message.channel.send(embed=embed)
        return
    
    elif message.content.startswith("$addstocktxt"):
        isAuthor = await util_function.isAuthor(str(message.author.id), client_data.OWNER_ID)
        if isAuthor['status'] == 400:
            return

        split_command = message.content.split()  # Split the command by whitespace

        if len(split_command) == 1:
            await message.channel.send(embed=await discordembed.textembed(f'$addstocktxt <productid>'))
            return
        
        if len(split_command) > 2:
            return
        
        productid = split_command[1]  # Access the second element (index 1)
        
        # Check for attachments
        if message.attachments:
            # Process the first attached file
            attachment = message.attachments[0]
            
            # Ensure it's a text file
            if attachment.filename.endswith('.txt'):
                # Download the file
                try:
                    file = await attachment.read()
                    content = file.decode('utf-8')  # Decode bytes to string assuming utf-8 encoding
                    
                    newstock = content.splitlines()
                    # Process 'content' here (e.g., write to a file, parse data, etc.)
                    # For demonstration, let's just print the content
                    request = await mongo.addstockbulk(productid, newstock)
                    await message.channel.send(embed=await discordembed.textembed(f'{request}'))
                    
                except Exception as e:
                    print(f"Error reading attachment: {e}")
            else:
                await message.channel.send(embed=await discordembed.textembed(f'Please attach a .txt file'))
        else:
            await message.channel.send(embed=await discordembed.textembed(f'You need to attach a text file'))
        return

    if message.embeds:
        webhook = await mongo.getwebhookid()
        if webhook['status'] == 400:
            print(webhook['message'])
            return
        if webhook['webhookid'] != str(message.author.id):
            return
        array = []
        for embed in message.embeds:
            desc = embed.description
            _array = desc.split('\n')
            array.extend(_array)

        pattern = r"Growid: (\S+)"
        pattern2 = r"Amount:\s+(.*)"

        # Retrieve 'growid' and 'amount' from the specified array indexes
        match = re.search(pattern, array[0])
        match2 = re.search(pattern2, array[1])

        # Extract 'amount' until 'Lock'
        lock_index = match2.group(1).find('Lock')
        cleaned_str = match2.group(1)[:lock_index + len('Lock')].strip()

        parse_amount = await util_function.parse_amount_and_type(cleaned_str)

        if parse_amount['status'] == 400:
            return

        newdonate = {
            'growid': match.group(1),
            'amount': parse_amount['amount']
        }
        addbal = await mongo.givebal(newdonate['growid'], 'worldlock', newdonate['amount'])

        assets = await mongo.getassets()
        assets = assets['assets']

        if addbal['status'] == 400:
            owner = bot.get_user(int(client_data.OWNER_ID))
            await owner.send(embed=await discordembed.secondtextembed(f'{newdonate["growid"]} deposit failed to be processed, amount: {newdonate["amount"]} {assets["sticker_4"]}!'))
            return
        
        user = bot.get_user(int(addbal['data']['discordid']))
        await user.send(embed=await discordembed.secondtextembed(f'Your deposit has been processed, amount: {newdonate["amount"]} {assets["sticker_4"]}!', 'Deposit Success'))
        
    await bot.process_commands(message)

def startBot():
    bot.run(client_data.TOKEN)
