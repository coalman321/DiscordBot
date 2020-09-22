import discord
import asyncio
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('C:\\Users\\Cole Tucker\\Downloads\\a-testproject-86d51-firebase-adminsdk-mcs7z-2b25a861d1.json')
defaultapp = firebase_admin.initialize_app(cred,  {'databaseURL': 'https://a-testproject-86d51.firebaseio.com'})

client = discord.Client()
user = 'Modbot'
disuser = db.reference('Users/' + user + '/Auth').get() #grab bot token from DB
print(disuser)


@client.event
async def on_ready():
    print('Logged in as: ' + client.user.name)
    #print(client.user.id)
    do_refresh()

@client.event
async def on_message(message):
    #print(get_emote_by_name("Brick", message))
    if message.author == client.user:
        return
    for com in commands:
        if com in message.content:
            dbresp = db.reference('Users/' + user + '/Commands/' + com).get()
            if len(message.mentions) > 0:
                await client.send_message(message.channel, dbresp.format(message, list(message.mentions)[0]))
            else:
                await client.send_message(message.channel, dbresp.format(message))
    if has_priveledge(message.author):
        for role in priv_roles:
            if has_role(message.author, role):
                dbcommresp = db.reference('Users/' + user + '/PrivCommands/' + role).get()
                for com in dbcommresp:
                    if com in message.content:
                        #print('com found ' + com)
                        dbresp = db.reference('Users/' + user + '/PrivCommands/' + role + '/' + com).get()
                        if 'refresh' in com:
                            do_refresh()
                        if 'assigned role' in dbresp and len(message.mentions) > 0:
                            await client.add_roles(list(message.mentions)[0], get_role_by_name(dbresp[dbresp.find('"') + 1: len(dbresp)-1], message))
                        if len(message.mentions) > 0:
                            await client.send_message(message.channel, dbresp.format(message, list(message.mentions)[0]))
                        else:
                            await client.send_message(message.channel, dbresp.format(message))



@client.event
async def on_message_edit(before, after):
    action_pef = False
    for action in on_edit:
        if action in after.content and action != 'default':
            print('non default action')
            dbresp = db.reference('Users/' + user + '/OnEdit/' + action)
            action_pef = True
    if not action_pef:
        dbresp = db.reference('Users/' + user + '/OnEdit/default').get()
        await client.add_reaction(after,get_emote_by_name(dbresp, after))

def do_refresh():
    global commands, emoji, priv_roles, on_edit
    commands = db.reference('Users/' + user + '/Commands/').get()
    priv_roles = db.reference('Users/' + user + '/PrivCommands').get(shallow=True)
    on_edit = db.reference('Users/' + user + '/OnEdit').get()
    emoji = list(client.get_all_emojis())


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

def get_role_by_name(name, message):
    for role in list(message.server.roles):
        if role.name == name:
            return role
    return None

def get_emote_by_name(name, message):
    for emo in emoji:
        if emo.name == name:
            return emo
    return None

client.run(disuser)
