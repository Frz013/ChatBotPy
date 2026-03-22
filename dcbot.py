import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import io
from image import edit_images

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot berhasil login sebagai {bot.user}!')
    print('------')


@bot.command()
async def halo(ctx):
    await ctx.send(f'Halo {ctx.author.mention}! Bot Anda sudah berfungsi dengan baik.')

@bot.command()
async def edit(ctx, *, user_prompt: str = None):

    if user_prompt is None:
        await ctx.send("Tolong masukkan prompt anda!")
        return

    if not ctx.message.attachments:
        await ctx.send("Tolong lampirkan sebuah gambar bersama dengan command tersebut!")
        return
    
    attachment = ctx.message.attachments[0]
    images_url = attachment.url
    if not attachment.content_type.startswith('image/'):
        await ctx.send("File yang dilampirkan harus berupa gambar!")
        return
    
    embed_input = discord.Embed(
            title="Prompt",
            description=user_prompt,
            color=discord.Color.green()
        )
    embed_input.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
    embed_input.set_image(url=images_url)
    embed_input.set_footer(text="Bot System • 2026")


    await ctx.reply(embed=embed_input)
    await ctx.send("Gambar sedang diproses...")

    images_result, result_images_url = edit_images(user_prompt, images_url)


    output_file = discord.File(images_result, filename="images_result.png")
    await ctx.reply("hasil edit: ", file=output_file)




bot.run(token)