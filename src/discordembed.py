import discord
import util_function

async def infoembed(field, assets, footer):
    siren = assets.get('sticker_1')
    arrow = assets.get('sticker_2')
    money = assets.get('sticker_3')
    worldlock = assets.get('sticker_4')
    crown = assets.get('sticker_5')
    embed = discord.Embed(
        title="",
        description="",
        color=0x0e0808
    )
    embed.add_field(
        name=f"{siren} **User Information** {siren}",
        value=f"{crown} **Registered GrowID** :\n{arrow} {field.get('growid')}\n{crown} **Your balance :** \n{arrow} {field.get('worldlock').get('balance')} {worldlock}\n{assets.get('sticker_2')} {util_function.rupiah_format(field.get('rupiah').get('balance'))} {money}", inline=True
        )
    embed.set_image(url=assets.get('bannerurl'))
    embed.set_footer(text=f"{footer.get('name')} | {footer.get('time')}", icon_url=footer.get('avatar'))
    return embed

async def showembed(listassets, assets, footer):
    embed = discord.Embed(
        title="",
        description="",
        color=0x0e0808
    )

    for data in listassets:
        embed.add_field(
            name=f"**Assets Code: {data.get('code')}**",
            value=f"{data.get('value')}", inline=True
            )
    embed.set_image(url=assets.get('bannerurl'))
    embed.set_footer(text=f"{footer.get('name')} | {footer.get('time')}", icon_url=footer.get('avatar'))
    return embed