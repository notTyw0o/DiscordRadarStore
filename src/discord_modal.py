import discord
import mongo
import discordembed
import util_function
import client_data
import asyncio
import hotmailbox

bot = discord.Bot()

class Register(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Grow ID"))

    async def callback(self, interaction: discord.Interaction):
        request = await mongo.register(interaction.user.id, self.children[0].value)
        await interaction.response.send_message(request, ephemeral=True)

class Order(discord.ui.Modal):
    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        

        self.add_item(discord.ui.InputText(label="Product Code"))
        self.add_item(discord.ui.InputText(label="Amount"))

    async def callback(self, interaction: discord.Interaction):
        try:
            int(self.children[1].value)
        except:
            embed = await discordembed.textembed('Amount must be an integer!')
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
        isOrder = await mongo.isOrder(self.children[0].value, int(self.children[1].value))
        isState = await mongo.checkstate()
        userBalance = await mongo.info(str(interaction.user.id))
        try:
            userBalance = userBalance['worldlock']['balance']
            totalprice = int(self.children[1].value) * int(isOrder['productdata']['productPrice'])
            isOrder['productdata']['amount'] = int(self.children[1].value)
            isOrder['productdata']['totalprice'] = totalprice
        except:
            embed = await discordembed.textembed(isOrder['message'])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if isOrder['status'] == 200 and isState['status'] == 200 and userBalance >= totalprice:
            await mongo.setorderstate('True')
            request = await mongo.takestock(self.children[0].value, int(self.children[1].value))
            asyncio.create_task(mongo.setorderstate('False'))
            if request['status'] == 200:
                removebalance = await mongo.give(str(interaction.user.id), 'worldlock', -totalprice)
                if "Success" in removebalance:
                    msg = ""
                    for text in request['data']:
                        msg += text + "\n"
                    assets = await mongo.getassets()
                    user = interaction.user
                    guild = interaction.guild
                    try:
                        footer = {'name': interaction.user.name,'time': await util_function.timenow(), 'avatar': interaction.user.avatar.url}
                    except:
                        footer = {'name': interaction.user.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                    embed = await discordembed.orderembed(isOrder['productdata'], assets['assets'], footer, str(interaction.user.id))
                    files = await util_function.write_text_file(f"== YOUR ORDER DETAILS ==\n{msg}", str(interaction.user.id))
                    file = discord.File(f'/home/Radar/txtfiles/{str(interaction.user.id)}.txt')
                    asyncio.create_task(user.send(file=file))
                    asyncio.create_task(user.send(embed=embed))
                    asyncio.create_task(util_function.delete_text_file(str(interaction.user.id)))
                    asyncio.create_task(mongo.addtotalspend(str(interaction.user.id), float(isOrder['productdata']['totalprice'])))
                    userlogs = {
                        'discordid': str(interaction.user.id), 
                        'productname': isOrder['productdata']['productName'],
                        'amount': str(isOrder['productdata']['amount']),
                        'totalprice': str(isOrder['productdata']['totalprice']),
                        'product': request['data']
                        }
                    asyncio.create_task(mongo.addlogs(userlogs))
                    try:
                        role = discord.utils.get(guild.roles, id=int(isOrder['productdata']['roleId']))
                        member = guild.get_member(user.id)
                        await member.add_roles(role)
                        arrow = assets['assets']['sticker_2']
                        responseembed = await discordembed.secondtextembed(f'{arrow} **Added new role : {role.name} ✅**\n{arrow} **Status : Success ✅**\n**Please check Direct Messages!**', 'Order Success')
                        asyncio.create_task(interaction.response.send_message(embed=responseembed, ephemeral=True))
                    except Exception as e:
                        arrow = assets['assets']['sticker_2']
                        responseembed = await discordembed.secondtextembed(f'{arrow} **Added new role : ❌**\n{arrow} **Status : Success ✅**\n**Please check Direct Messages!**', 'Order Success')
                        asyncio.create_task(interaction.response.send_message(embed=responseembed, ephemeral=True))
                    channelid = await mongo.getchannelhistory()
                    if channelid['status'] == 200:
                        channel = guild.get_channel(int(channelid['data']))
                        asyncio.create_task(channel.send(embed=embed))
                    else:
                        pass
                else:
                    await mongo.setorderstate('False')
                    await interaction.response.send_message(removebalance, ephemeral=True)
            else:
                await mongo.setorderstate('False')
                await interaction.response.send_message(request['message'], ephemeral=True)
        elif isOrder['status'] == 400:
            await interaction.response.send_message(isOrder['message'], ephemeral=True)
        elif isState['status'] == 400:
            await interaction.response.send_message(isState['message'], ephemeral=True)
        elif userBalance < totalprice:
            await interaction.response.send_message(f'Insufficient balance!', ephemeral=True)

class OrderEmail(discord.ui.Modal):
    def __init__(self, bot, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        

        self.add_item(discord.ui.InputText(label="Product Code"))
        self.add_item(discord.ui.InputText(label="Amount"))

    async def callback(self, interaction: discord.Interaction):
        userBalance = await mongo.info(str(interaction.user.id))
        if userBalance['status'] == 400:
            embed = await discordembed.textembed(userBalance['message'])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        codedata = [
            {'code': 1, 'productcode': 'HOTMAIL', 'minorder': 1, 'price': 1},
            {'code': 2, 'productcode': 'OUTLOOK', 'minorder': 1, 'price': 1},
            {'code': 3, 'productcode': 'HOTMAIL.TRUSTED', 'minorder': 10, 'price': 7},
            {'code': 4, 'productcode': 'OUTLOOK.TRUSTED', 'minorder': 10, 'price': 7},
            {'code': 5, 'productcode': 'HOTMAIL.PVA', 'minorder': 10, 'price': 10},
            {'code': 6, 'productcode': 'OUTLOOK.PVA', 'minorder': 10, 'price': 10},
        ]

        selectedproduct = []
        for codes in codedata:
            if codes['code'] == int(self.children[0].value):
                selectedproduct.append(codes)

        if len(selectedproduct) == 0:
            embed = await discordembed.textembed('Product code is not valid!')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        elif int(self.children[1].value) < selectedproduct[0]['minorder']:
            embed = await discordembed.textembed(f'Does not meet the minimum order requirement!')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        balance = userBalance['worldlock']['balance']
        totalprice = selectedproduct[0]['price']*int(self.children[1].value)
        if balance < totalprice:
            embed = await discordembed.textembed(f'Insufficient balance!')
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        request = await hotmailbox.order(selectedproduct[0]['productcode'], int(self.children[1].value), totalprice)
        if request['status'] == 400:
            embed = await discordembed.textembed(request['message'])
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await mongo.give(str(interaction.user.id), 'worldlock', -totalprice)

        try:
            footer = {'name': interaction.user.name,'time': await util_function.timenow(), 'avatar': interaction.user.avatar.url}
        except:
            footer = {'name': interaction.user.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
       
        data = {'productName': request['data']['Product'], 'amount': request['data']['Quantity'], 'totalprice': totalprice}
        assets = await mongo.getassets()
        embed = await discordembed.orderembed(data, assets['assets'], footer, str(interaction.user.id))

        msg = ""
        for messages in request['data']['Emails']:
            msg += f'{messages["Email"]}:{messages["Password"]}\n'

        files = await util_function.write_text_file(f"== YOUR ORDER DETAILS ==\n{msg}", str(interaction.user.id))
        file = discord.File(f'/home/Radar/txtfiles/{str(interaction.user.id)}.txt')

        userlogs = {
            'discordid': str(interaction.user.id), 
            'productname': request['data']['Product'],
            'amount': str(request['data']['Quantity']),
            'totalprice': totalprice,
            'product': request['data']['Emails']
            }
        
        user = interaction.user
        guild = interaction.guild

        asyncio.create_task(mongo.addlogs(userlogs))
        asyncio.create_task(user.send(file=file))
        asyncio.create_task(user.send(embed=embed))
        asyncio.create_task(util_function.delete_text_file(str(interaction.user.id)))

        try:
            role = discord.utils.get(guild.roles, id=1176753211101687899)
            member = guild.get_member(user.id)
            await member.add_roles(role)
            arrow = assets['assets']['sticker_2']
            responseembed = await discordembed.secondtextembed(f'{arrow} **Added new role : {role.name} ✅**\n{arrow} **Status : Success ✅**\n**Please check Direct Messages!**', 'Order Success')
            asyncio.create_task(interaction.response.send_message(embed=responseembed, ephemeral=True))
        except Exception as e:
            arrow = assets['assets']['sticker_2']
            responseembed = await discordembed.secondtextembed(f'{arrow} **Added new role : ❌**\n{arrow} **Status : Success ✅**\n**Please check Direct Messages!**', 'Order Success')
            asyncio.create_task(interaction.response.send_message(embed=responseembed, ephemeral=True))
        channelid = await mongo.getchannelhistory()
        if channelid['status'] == 200:
            channel = guild.get_channel(int(channelid['data']))
            asyncio.create_task(channel.send(embed=embed))
        else:
            pass
    
class RegisterLicense(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Discord Token"))
        self.add_item(discord.ui.InputText(label="Secret Password"))

    async def callback(self, interaction: discord.Interaction):
        userbalance = await mongo.info(str(interaction.user.id))
        userbalance = userbalance['worldlock']['balance']
        check = await mongo.isOrderlisen('botlisen', 1)
        if check['status'] == 200 and userbalance >= check['productdata']['productPrice']:
            await mongo.removestocklisen('botlisen', 0, False)
            await mongo.give(interaction.user.id,'worldlock', -check['productdata']['productPrice'])
            secretkey = util_function.generatemd5(str(interaction.user.id) + self.children[1].value)
            license = util_function.generate_random_string(10)
            request = await mongo.registerbot(self.children[0].value, str(interaction.user.id), license, secretkey)
            if request['status'] == 200:
                user = interaction.user
                line = "-------------------------"
                await user.send(f"```Thank you for purchasing\n{line}\nOrder details\n-> License : {license}\n-> Secretkey : {secretkey} *DO NOT SHARE\n{line}\nFor further assistance, contact owner!```")
                try:
                    guild = interaction.guild
                    role = discord.utils.get(guild.roles, id=int(check['productdata']['roleId']))
                    member = guild.get_member(user.id)
                    await member.add_roles(role)
                    embed = await discordembed.textembed(f"Success add new role, Please check your direct messages!")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                except Exception as e:
                    embed = await discordembed.textembed(f"Success, Please check your direct messages!")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.response.send_message(request['message'], ephemeral=True)
        else:
            await interaction.response.send_message(f'Error occured!', ephemeral=True)

class Claim(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Secret key"))
        self.add_item(discord.ui.InputText(label="License"))

    async def callback(self, interaction: discord.Interaction):
        request = await mongo.claim(self.children[0].value, self.children[1].value)
        if request['status'] == 200:
            await interaction.response.send_message(request['message'], ephemeral=True)
        else:
            await interaction.response.send_message(request['message'], ephemeral=True)

class Start(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Secret key"))

    async def callback(self, interaction: discord.Interaction):
        request = await util_function.startbot(self.children[0].value)
        if request['status'] == 200:
            await interaction.response.send_message(request['message'], ephemeral=True)
        else:
            await interaction.response.send_message(request['message'], ephemeral=True)

class Off(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Secret key"))

    async def callback(self, interaction: discord.Interaction):
        if self.children[0].value in ['API', 'RadarStoreHelper']:
            await interaction.response.send_message(f'Error!', ephemeral=True)
        else:
            request = await util_function.offbot(self.children[0].value)
            if request['status'] == 200:
                await interaction.response.send_message(request['message'], ephemeral=True)
            else:
                await interaction.response.send_message(request['message'], ephemeral=True)

class Restart(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Secret key"))

    async def callback(self, interaction: discord.Interaction):
        if self.children[0].value in ['API', 'RadarStoreHelper']:
            await interaction.response.send_message(f'Error!', ephemeral=True)
        else:
            request = await util_function.restartbot(self.children[0].value)
            if request['status'] == 200:
                await interaction.response.send_message(request['message'], ephemeral=True)
            else:
                await interaction.response.send_message(request['message'], ephemeral=True)

            

