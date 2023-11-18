import discord
import mongo
import discordembed
import util_function
import client_data

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
        isOrder = await mongo.isOrder(self.children[0].value, int(self.children[1].value))
        isState = await mongo.checkstate()
        userBalance = await mongo.info(str(interaction.user.id))

        try:
            userBalance = userBalance['worldlock']['balance']
            totalprice = int(self.children[1].value) * int(isOrder['productdata']['productPrice'])
            isOrder['productdata']['amount'] = int(self.children[1].value)
            isOrder['productdata']['totalprice'] = totalprice
        except:
            await interaction.response.send_message('Insufficient stock!', ephemeral=True)
            return

        if isOrder['status'] == 200 and isState['status'] == 200 and userBalance >= totalprice:
            await mongo.setorderstate('True')
            request = await mongo.takestock(self.children[0].value, int(self.children[1].value))
            if request['status'] == 200:
                removebalance = await mongo.give(str(interaction.user.id), 'worldlock', -totalprice)
                if "Success" in removebalance:
                    await mongo.setorderstate('False')
                    assets = await mongo.getassets()
                    user = interaction.user
                    guild = interaction.guild
                    try:
                        footer = {'name': interaction.user.name,'time': await util_function.timenow(), 'avatar': interaction.user.avatar.url}
                    except:
                        footer = {'name': interaction.user.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                    embed = await discordembed.orderembed(isOrder['productdata'], assets['assets'], footer, str(interaction.user.id))
                    files = util_function.write_text_file(f"== YOUR ORDER DETAILS ==\n{request['message']}")
                    file = discord.File(f'/home/Radar/txtfiles/{client_data.SECRET_KEY}.txt')
                    await user.send(file=file)
                    await user.send(embed=embed)
                    util_function.delete_text_file()
                    userlogs = {
                        'discordid': str(interaction.user.id), 
                        'productname': isOrder['productdata']['productName'],
                        'amount': str(isOrder['productdata']['amount']),
                        'totalprice': str(isOrder['productdata']['totalprice']),
                        'product': request['message']
                        }
                    await mongo.addlogs(userlogs)
                    try:
                        role = discord.utils.get(guild.roles, id=int(isOrder['productdata']['roleId']))
                        member = guild.get_member(user.id)
                        await member.add_roles(role)
                        await interaction.response.send_message("Success add new role\nCheck your direct messages!", ephemeral=True)
                    except Exception as e:
                        await interaction.response.send_message("Check your direct messages!", ephemeral=True)
                    channelid = await mongo.getchannelhistory()
                    if channelid['status'] == 200:
                        channel = guild.get_channel(int(channelid['data']))
                        await channel.send(embed=embed)
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

            

