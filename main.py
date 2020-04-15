import discord
import asyncio

client = discord.Client()

def get_voice_channel(member):
    for channel in client.guilds[0].voice_channels:
        for temp_member in channel.members:
            if member == temp_member:
                return channel
    return None

def find_voice_channel(name):
    print(client.guilds[0].voice_channels)
    for channel in client.guilds[0].voice_channels:
        print("{} compared to {}".format(channel.name, name))
        if channel.name == name:
            return channel
    return None

conditions = {'tg':{
                'max_time':15,
                'min_time':2,
                'max_length':3,
                'forbidden_users':{
                'Cotontiges'
                    },
                'forbidden_receivers':{
                'La Distance',
                    },
                }
     }

@client.event
async def on_ready():
    print('Logged on as {0}!'.format(client.user))

@client.event
async def on_message(message):
    print('Message from {0.author}: {0.content}'.format(message))
    if "bonjour bot" in message.content.lower():
        await message.channel.send("Bonjour !")


    elif "!getguild" in message.content.lower():
        print(client.guilds)

    elif message.content.lower().startswith("!tg"):
        message_info = message.content.split(" ")

        if len(message_info)>conditions['tg']['max_length']:
            message_info[1]=" ".join(message_info[1:-1])
            print(message_info[1])
            message_info = [message_info[0], message_info[1], int(message_info[-1])]
            print(message_info)
        # sale
        message_info[2] = int(message_info[2])

        muted_member = None
        if message_info[2]>conditions['tg']['max_time']:
            message_info[2]=conditions['tg']['max_time']
            muted_member = message.author
        elif message_info[2]<conditions['tg']['min_time']:
            message_info[2]=conditions['tg']['min_time']


        if message.author.name in conditions['tg']['forbidden_users']:
            await message.channel.send("On vous a retiré le droit d'utiliser cette commande. Tocard !")

        elif message_info[1] in conditions['tg']['forbidden_receivers']:
            await message.channel.send("Vous ne pouvez pas mute {}.".format(message_info[1]))

        elif muted_member == message.author:
            await message.channel.send("Tu as abusé de la commande : elle se retourne contre toi. BIM")
            await muted_member.edit(mute=True)
            await asyncio.sleep(int(message_info[2]))
            await message.channel.send("Bon, je te démute {}... Mais c'est bien parce que c'est toi !".format(muted_member.name))
            await member.edit(mute=False)

        else:
            for muted_member in client.guilds[0].members:
                if muted_member.name.lower() == message_info[1].lower():
                    await message.channel.send("Ta gueule {} ! Tu n'as plus le droit de parler pendant {} secondes.".format(muted_member.name, message_info[2]), tts=True)
                    await muted_member.edit(mute=True)
                    await asyncio.sleep(int(message_info[2]))
                    await message.channel.send("Bon, je te démute {}... Mais c'est bien parce que c'est toi !".format(muted_member.name))
                    await muted_member.edit(mute=False)

    elif message.content.startswith("!moveall"):
        message_info = message.content.split(" ")
        if len(message_info)>2:
            channelname = " ".join(message_info[1:])
        message_info = [message_info[0], channelname]

        initial_channel = get_voice_channel(message.author)
        destination_channel = find_voice_channel(message_info[1])
        for member in initial_channel.members:
            await member.edit(voice_channel = destination_channel)
        await message.channel.send("Déplacement de toutes les personnes du channel {} vers le channel {}.".format(initial_channel, destination_channel))

    elif message.content.startswith("!clearplays"):
        await message.channel.send("Suppression de tous les !play dans ce channel.")
        async for msg in message.channel.history()
            if msg.content.startswith("!play") or msg.author.name.lower()=="La Rythmance".lower():
                await msg.delete()
        await message.channel.send("Messages supprimés.")


client.run('NjkxMzE1MDA2NTE5OTAyMjYw.XpdX7Q._bUSZnooXTaIk5o_RhfFAb1IsaY')
