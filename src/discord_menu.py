import discord
import mongo
import client_data
import discord_modal as modal
import discordembed
import discord_button
import util_function

bot = discord.Bot(intents=discord.Intents.all())


class MainView(discord.ui.View):
    @discord.ui.select(
        placeholder = "Hello, choose command here!",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="None",
                description="None"
            ),
            discord.SelectOption(
                label="Register Grow ID",
                description="Register your Grow ID!"
            ),
            discord.SelectOption(
                label="User Information",
                description="Get your user information!"
            ),
            discord.SelectOption(
                label="Deposit Information",
                description="Get deposit information!"
            ),
            discord.SelectOption(
                label="Order Product",
                description="Order an product!"
            ),
            discord.SelectOption(
                label="Check Stock",
                description="Check available stock on store!"
            )
        ]
    )
    async def select_callback(self, select, interaction):
        isActive = await mongo.checkOwner(client_data.SECRET_KEY)
        selectedvalues = select.values[0]
        if isActive['status'] == 200:
            if selectedvalues == "None":
                await interaction.response.send_message('Nothing!', ephemeral=True)
            elif selectedvalues == "Register Grow ID":
                await interaction.response.send_modal(modal.Register(title=select.values[0]))
            elif selectedvalues == "User Information":
                userid = str(interaction.user.id)
                request = await mongo.info(userid)
                template = await mongo.getassets()
                if request.get('status') == 200 and template.get('status') == 200:
                    try:
                        footer = {'name': interaction.user.name,'time': await util_function.timenow(), 'avatar': interaction.user.avatar.url}
                    except:
                        footer = {'name': interaction.user.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                    embed = await discordembed.infoembed(request, template.get('assets'), footer)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                elif request.get('status') == 400:
                    await interaction.response.send_message(request.get('message'), ephemeral=True)
                elif template.get('status') == 400:
                    await interaction.response.send_message(template.get('message'), ephemeral=True)
            elif selectedvalues == "Deposit Information":
                request = await mongo.getdeposit()
                template = await mongo.getassets()
                if request.get('status') == 200 and template.get('status') == 200:
                    try:
                        footer = {'name': interaction.user.name,'time': await util_function.timenow(), 'avatar': interaction.user.avatar.url}
                    except:
                        footer = {'name': interaction.user.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                    embed = await discordembed.depositembed(request, template.get('assets'), footer)
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                elif request.get('status') == 400:
                    await interaction.response.send_message(request.get('message'), ephemeral=True)
                elif template.get('status') == 400:
                    await interaction.response.send_message(template.get('message'), ephemeral=True)
            elif selectedvalues == "Order Product":
                await interaction.response.send_modal(modal.Order(bot, title=select.values[0]))
            elif selectedvalues == "Check Stock":
                request = await mongo.checkstock()
                template = await mongo.getassets()
                if request.get('status') == 200 and template.get('status') == 200:
                    try:
                        footer = {'name': interaction.user.name,'time': await util_function.timenow(), 'avatar': interaction.user.avatar.url}
                    except:
                        footer = {'name': interaction.user.name, 'time': await util_function.timenow(), 'avatar': 'https://archive.org/download/discordprofilepictures/discordgrey.png'}
                    embed = await discordembed.checkstockembed(request, template.get('assets'), footer)
                    await interaction.response.send_message(embed=embed, view=discord_button.OrderButton(timeout=None),  ephemeral=True)
                elif request.get('status') == 400:
                    await interaction.response.send_message(request.get('message'), ephemeral=True)
                elif template.get('status') == 400:
                    await interaction.response.send_message(template.get('message'), ephemeral=True)
            else:
                await interaction.response.send_message('Not yet set!', ephemeral=True)
        else:
            await interaction.response.send_message(isActive['message'], ephemeral=True)

    

