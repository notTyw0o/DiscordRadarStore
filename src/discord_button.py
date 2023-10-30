import discord
import discord_modal

bot = discord.Bot()

class OrderButton(discord.ui.View):
    @discord.ui.button(label="Order here!", row=0, style=discord.ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(discord_modal.Order(title='Order Products!'))