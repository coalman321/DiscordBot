import discord
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

user = 'AnotherUser'

cred = credentials.Certificate('C:\\Users\\Cole Tucker\\Downloads\\a-testproject-86d51-firebase-adminsdk-mcs7z-2b25a861d1.json')
defaultapp = firebase_admin.initialize_app(cred,  {'databaseURL': 'https://a-testproject-86d51.firebaseio.com'})

client = discord.Client()
disuser = db.reference('Users/' + user + '/Auth').get() #grab bot token from DB

@client.event
async def on_ready():
    print('Logged in as: ' + client.user.name)
    do_refresh()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    for cmd in commands:
        # try:
            command_name = db.reference('Users/' + user + '/Commands/' + cmd + '/Name').get()
            if command_name in message.content:
                print(command_name)

                internal_cmd = db.reference('Users/' + user + '/Commands/' + cmd + '/Command').get()
                print(internal_cmd)
                if 'reload' in internal_cmd:
                    do_refresh()
                elif 'assign' in internal_cmd:
                    await assign_user_role(list(message.mentions)[0], get_role_by_name(internal_cmd[7:], message))
                elif 'remove' in internal_cmd:
                    await del_user_role(list(message.mentions)[0], get_role_by_name(internal_cmd[7:], message))

                user_out = str(db.reference('Users/' + user + '/Commands/' + cmd + '/Message').get())
                if len(message.mentions) > 0:
                    await message.channel.send(user_out.format(message, list(message.mentions)[0]))
                else:
                    await message.channel.send(user_out.format(message))
        # except:
            # print('lookup failed')

    if has_priveledge(message.author):
        for role in priv_roles:
            if has_role(message.author, role):
                role_commands = db.reference('Users/' + user + '/PrivCommands/' + role).get()
                for role_command in role_commands:
                    role_command_name = db.reference('Users/' + user + '/PrivCommands/' + role + '/' + role_command + '/Name').get()
                    if message.content.startswith(role_command_name):
                        user_out = db.reference('Users/' + user + '/PrivCommands/' + role + '/' + role_command + '/Message').get()

                        internal_cmd = db.reference('Users/' + user + '/PrivCommands/' + role + '/' + role_command + '/Command').get()
                        print(internal_cmd)
                        if 'reload' in internal_cmd:
                            do_refresh()
                        elif 'assign' in internal_cmd:
                            await assign_user_role(list(message.mentions)[0],
                                                   get_role_by_name(internal_cmd[7:], message))
                        elif 'remove' in internal_cmd:
                            await del_user_role(list(message.mentions)[0], get_role_by_name(internal_cmd[7:], message))

                        if len(message.mentions) > 0:
                            await message.channel.send(user_out.format(message, list(message.mentions)[0]))
                        else:
                            await message.channel.send(user_out.format(message))



@client.event
async def on_message_edit(before, after):
    print('no-op')

def do_refresh():
    global emoji, priv_roles, on_edit, commands
    print('reloading globals from DB')
    commands = db.reference('Users/' + user + '/Commands').get()
    priv_roles = db.reference('Users/' + user + '/PrivCommands').get(shallow=True)
    on_edit = db.reference('Users/' + user + '/OnEdit').get()
    emoji = list(client.emojis)


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
    for role in list(message.guild.roles):
        if role.name == name:
            return role
    return None


def get_emote_by_name(name, message):
    for emo in emoji:
        if emo.name == name:
            return emo
    return None


async def assign_user_role(user, role):
    await user.add_roles(role)


async def del_user_role(user, role):
    await user.remove_roles(role)


client.run(disuser)