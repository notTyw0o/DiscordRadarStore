import discord
import mongo
import client_data

class Register(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="Grow ID"))

    async def callback(self, interaction: discord.Interaction):
        request = await mongo.register(interaction.user.id, self.children[0].value)
        await interaction.response.send_message(request, ephemeral=True)

