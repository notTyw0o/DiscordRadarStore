import discord
import mongo
import discordembed
import util_function


class Register(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Grow ID"))

    async def callback(self, interaction: discord.Interaction):
        request = await mongo.register(interaction.user.id, self.children[0].value)
        await interaction.response.send_message(request, ephemeral=True)

class Order(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        

        self.add_item(discord.ui.InputText(label="Product Code"))
        self.add_item(discord.ui.InputText(label="Amount"))

    async def callback(self, interaction: discord.Interaction):
        isOrder = await mongo.isOrder(self.children[0].value, int(self.children[1].value))
        isState = await mongo.checkstate()
        userBalance = await mongo.info(str(interaction.user.id))

        userBalance = userBalance['worldlock']['balance']
        totalprice = int(self.children[1].value) * int(isOrder['productdata']['productPrice'])
        isOrder['productdata']['amount'] = int(self.children[1].value)
        isOrder['productdata']['totalprice'] = totalprice

        if isOrder['status'] == 200 and isState['status'] == 200 and userBalance >= totalprice:
            await mongo.setorderstate('True')
            request = await mongo.takestock(self.children[0].value, int(self.children[1].value))
            if request['status'] == 200:
                removebalance = await mongo.give(str(interaction.user.id), 'worldlock', -totalprice)
                if "Success" in removebalance:
                    await mongo.setorderstate('False')
                    assets = await mongo.getassets()
                    user = interaction.user
                    try:
                        footer = {'name': interaction.user.name,'time': await util_function.timenow(), 'avatar': interaction.user.avatar.url}
                    except:
                        footer = {'name': interaction.user.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                    embed = await discordembed.orderembed(isOrder['productdata'], assets['assets'], footer)
                    await user.send(f"```{request['message']}```")
                    await user.send(embed=embed)
                    await interaction.response.send_message("Check your direct messages!", ephemeral=True)
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
            await interaction.response.send_message('Insufficient Balance!', ephemeral=True)

