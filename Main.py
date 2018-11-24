import discord
import asyncio
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('C:\\Users\\Cole Tucker\\Downloads\\a-testproject-86d51-firebase-adminsdk-mcs7z-2b25a861d1.json')
defaultapp = firebase_admin.initialize_app(cred,  {'databaseURL': 'https://a-testproject-86d51.firebaseio.com'})

client = discord.Client()
user = db.reference('Users/Modbot/Auth').get() #grab bot token from DB
print(user)

@client.event
async def on_ready():
    print('Logged in as: ' + client.user.name)
    print(client.user.id)
    do_refresh()

@client.event
async def on_message(message):
    print(has_priveledge(message.author))
    if message.author == client.user:
        return
    for com in commands:
        if com in message.content:
            dbresp = db.reference('Users/Modbot/Commands/' + com).get()
            msg = dbresp.format(message)
            await client.send_message(message.channel, msg)
    if has_priveledge(message.author):
        for role in priv_roles:
            if has_role(message.author, role):
                print('author has ' + role)
                dbresp = db.reference('Users/Modbot/PrivCommands/' + role).get()
                print(dbresp)


@client.event
async def on_message_edit(before, after):
    print('user edited message')
    await client.add_reaction(after,emoji[9])

def do_refresh():
    global commands, emoji, priv_roles
    commands = db.reference('Users/Modbot/Commands/').get()
    priv_roles = db.reference('Users/Modbot/PrivCommands').get(shallow=True)
    emoji = list(client.get_all_emojis())
    #print(commands)
    for emo in emoji:
       print(emo)
    for com in priv_roles:
        print(com)

def has_role(user, check_role):
    for role in user.roles:
        if role.name in check_role:
            return True
    return False

def has_priveledge(user):
    to_ret = False
    for role in priv_roles:
        to_ret |= has_role(user, role)
    return to_ret



client.run(user)
