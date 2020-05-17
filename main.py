import discord
from discord.ext import commands
import asyncio
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('la-botance-e472e977a24e.json')
firebase_admin.initialize_app(cred)
client = discord.Client()

db = firestore.client()

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
def get_member_id(name):
    for member in client.guilds[0].members:
        if member.name == name:
            return member.id
    return None
def find_text_channel(name):
    for channel in client.guilds[0].text_channels:
        if channel.name == name:
            return channel
    return None

def determine_nickname(member):
    if member.nick is None:
        return str(member)[:-5]
    return member.nick
async def get_dm_channel(member):
    if member.dm_channel is None:
        await member.create_dm()
    return member.dm_channel

async def update_lg_database():
    # iterator of users collection
    users_docs = db.collection(u'extensions').document(u'loup-garance').collection(u'users').stream()
    text_channel = find_text_channel("inscriptions-loup-garance")
    # creating list of all registered users
    async for msg in text_channel.history(limit=1):
        for reaction in msg.reactions:
            if reaction.emoji == '👍' :
                users_discord = await reaction.users().flatten()
                usernames_discord = [user.name for user in users_discord]

    # dirty
    db_usernames_list = []
    #First loop : create temp list of existing usernames, but also delete people who unregistered themselves.
    for user in users_docs:
        username = user.to_dict()["name"]
        if username in usernames_discord:
            db_usernames_list.append(username)
        else:
            db.collection(u'extensions').document(u'loup-garance').collection(u'users').document(username).delete()
    # Second loop : compare usernames with temp list of existing usernames, add user if not in list.
    for username in usernames_discord:
        if username not in db_usernames_list:
            new_user = {u'name': username}
            db.collection(u'extensions').document(u'loup-garance').collection(u'users').document(username).set(new_user)

    print("Updated database")

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
async def on_voice_state_update(member, before, after):
    text_channel_id = find_text_channel("connexions")
    nickname = determine_nickname(member)
    if text_channel_id is not None:
        if before.channel != after.channel:
            if after.channel is None:
                await client.guilds[0].text_channels[3].send("**{0}** : :red_circle: {1}".format(nickname, before.channel))
            elif before.channel is None:
                await client.guilds[0].text_channels[3].send("**{0}** : :green_circle: {1}".format(nickname, after.channel))
            elif before.channel is not None and after.channel is not None:
                await client.guilds[0].text_channels[3].send("**{0}** : :red_circle: {1} -> :green_circle: {2}".format(nickname, before.channel, after.channel))
@client.event
async def on_raw_reaction_add(payload):
    print("Caught reaction addition !")
    print("Payload chan id : {}, loup-garance id : {}".format(payload.channel_id, find_text_channel("inscriptions-loup-garance").id))
    if payload.channel_id == find_text_channel("inscriptions-loup-garance").id:
        await update_lg_database()
        print("Updated Firestore database.")

@client.event
async def on_raw_reaction_remove(payload):
    print("Caught reaction removal !")
    print("Payload chan id : {}, loup-garance id : {}".format(payload.channel_id, find_text_channel("inscriptions-loup-garance").id))
    if payload.channel_id == find_text_channel("inscriptions-loup-garance").id:
        await update_lg_database()
        print("Updated Firestore database.")

@client.event
async def on_message(message):
    print('Message from {0.author} (id : {0.author.id}): {0.content}'.format(message))
    if "bonjour bot" in message.content.lower():
        await message.channel.send("Bonjour !")

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
        if destination_channel is None:
            await message.channel.send("Ce channel n'existe pas.")
        else:
            for member in initial_channel.members:
                await member.edit(voice_channel = destination_channel)
            await message.channel.send("Déplacement de toutes les personnes du channel {} vers le channel {}.".format(initial_channel, destination_channel))

    elif message.content.startswith("!clearplays"):
        await message.channel.send("Suppression de tous les !play dans ce channel.")
        async for msg in message.channel.history(limit=None):
            if msg.content.startswith("!play") or msg.author.id == 235088799074484224: # ID of the Rythm bot
                print("Deleted this message : {}".format(msg.content))
                await msg.delete()
        await message.channel.send("Messages supprimés.")

    elif message.content.startswith("!update"):
        """ Used for manually updating the users, just in case."""
        await update_lg_database()
    elif message.content.startswith("!lg-send"):
        message_info = message.content.split('"')
        msg_to_send = message_info[1]
        # safety : update before sending
        await update_lg_database()
        users_docs = db.collection(u'extensions').document(u'loup-garance').collection(u'users').stream()
        for user in users_docs:
            username = user.to_dict()["name"]
            print(f"Username : {username}")
            member = client.guilds[0].get_member(get_member_id(username))
            channel = await get_dm_channel(member)
            await channel.send(msg_to_send)
            print(f"Sent message to {username}")
if __name__ == '__main__':
    import config
    client.run(config.token)
