import discord
from bota import constant
from bota.help import NOTE_FOOTER


def embed_txt_message(content, add_header=False, header=constant.DEFAULT_EMBED_HEADER, color=discord.Color.blue()):
    embed_msg = discord.Embed(description=content, color=color)
    if add_header:
        embed_msg.set_author(name=header['name'], icon_url=header['icon_url'], url=header['url'])
    return embed_msg


def prefix_validation_correct(string):
    if len(string) == 1 and string != '':
        return True
    return False


def add_footer_requested_by_username(embed, message, note=NOTE_FOOTER):
    try:
        user_discord_id = message.author.id
        user = message.guild.get_member(user_discord_id)
        embed.set_footer(text=f'Req by {message.author.name}{note}', icon_url=user.avatar_url)
        return embed
    except Exception as e:
        return embed


def get_infos_from_msg(ctx):
    message_string = str(ctx.message.content)
    message_word_length = message_string.split()
    user_discord_id = ctx.message.author.id
    user_discord_name = ctx.message.author.name

    return message_string, message_word_length, user_discord_id, user_discord_name

