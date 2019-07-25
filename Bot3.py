import discord
import pyodbc

botuser = 'MODBOT'
server = 'localhost'
database = 'Test'
commandtable = '.dbo.BotCommands'
authtable = '.dbo.BotUsers'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
cursor = cnxn.cursor()

cursor.execute('select BOTKEY from ' + database + authtable + ' where BOTNAME = \'' + botuser + '\'')
row = cursor.fetchone()

client = discord.Client()
disuser = row[0]

@client.event
async def on_ready():
    print('Logged in as: ' + client.user.name)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    query = 'Select * from Test.dbo.BotCommands where \'' + message.content + '\' like COMMAND;'
    cursor.execute(query)
    row = cursor.fetchone()

    while row:
        print(row)

        if not row[4] is None and not has_role(message.author, row[4]):
            await message.channel.send("User does not have sufficient permissions")
            return

        await process_command(message, row[2])

        user_out = row[1]
        if len(message.mentions) > 0:
            for user in message.mentions:
                await message.channel.send(user_out.format(message, user))
        else:
            await message.channel.send(user_out.format(message))

        row = cursor.fetchone()

@client.event
async def on_message_edit(before, after):
    print('no-op')

async def process_command(message, internal_cmd):
    if internal_cmd is None: return

    print(internal_cmd)


    if 'assign' in internal_cmd:
        await assign_user_role(list(message.mentions), get_role_by_name(internal_cmd[7:], message))

    elif 'remove' in internal_cmd:
        await del_user_role(list(message.mentions), get_role_by_name(internal_cmd[7:], message))

def has_role(user, check_role):
    for role in user.roles:
        if role.name in check_role:
            return True
    return False

def get_role_by_name(name, message):
    for role in list(message.guild.roles):
        if role.name == name:
            return role
    return None


def get_emote_by_name(name, message):
    for emo in list(client.emojis):
        if emo.name == name:
            return emo
    return None


async def assign_user_role(users, role):
    for user in users:
        await user.add_roles(role)


async def del_user_role(users, role):
    for user in users:
        await user.remove_roles(role)

client.run(disuser)