import discord
from discord.ext import commands
import asyncio
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('la-botance-e472e977a24e.json')
firebase_admin.initialize_app(cred)
bot = commands.Bot(command_prefix='!')

db = firestore.client()

def get_voice_channel(member):
    for channel in bot.guilds[0].voice_channels:
        for temp_member in channel.members:
            if member == temp_member:
                return channel
    return None

def find_voice_channel(name):
    print(bot.guilds[0].voice_channels)
    for channel in bot.guilds[0].voice_channels:
        print("{} compared to {}".format(channel.name, name))
        if channel.name == name:
            return channel
    return None

def find_text_channel(name):
    for channel in bot.guilds[0].text_channels:
        if channel.name == name:
            return channel
    return None

def determine_nickname(member):
    if member.nick is None:
        return str(member)[:-5]
    return member.nick


@bot.group()
async def lg(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Commande invalide pour l'extension Loup-Garance")

@lg.command()
async def send(ctx, message:str):
    # update list of registered users
    # fetch list of registered users
    # for each of those users :
    #   send message
    # send confirmation message on channel
    pass


@lg.command()
async def update(ctx):
    """ Used for manually updating the users, just in case."""
    text_channel_id = find_text_channel("inscriptions-loup-garance")
    # iterator of users collection
    users_docs = db.collection(u'extensions').document(u'loup-garance').collections(u'users').stream()

    # creating list of all registered users
    async for msg in bot.guilds[0].text_channels[text_channel_id].history(limit=1):
        async for reaction in msg.reactions:
            if reaction.emoji == '👍' :
                users_discord = await reaction.users().flatten()
                usernames_discord = [user.name for user in users_discord]


    # dirty
    db_usernames_list = []

    #First loop : create temp list of existing usernames, but also delete people who unregistered themselves.
    for user in user_docs:
        username = user.to_dict()["name"]
        if username in usernames_discord:
            db_usernames_list.append(username)
        else:
            user.delete()
    # Second loop : compare usernames with temp list of existing usernames, add user if not in list.
    for username in usernames_discord:
        if username not in db_usernames_list:
            new_user = {u'name': unicode(username)}
            db.collection(u'extensions').document(u'loup-garance').collections(u'users').add(new_user)

if __name__ == '__main__':
    import config
    bot.run(config.token)
