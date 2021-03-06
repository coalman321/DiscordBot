from queue import Queue
import time
import datetime
import discord
import pyodbc
import asyncio

#defined constants for base access
botuser = 'MODBOT'
server = 'localhost'
database = 'Test'
commandtable = '.dbo.BotCommands'
authtable = '.dbo.BotUsers'
bot_start = datetime.now()
up_time = datetime.timedelta()
sql_queue_out = Queue()

#estabish connection 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
cnxn.autocommit = False
cursor = cnxn.cursor()
cursor.execute('select BOTKEY from ' + database + authtable + ' where BOTNAME = \'' + botuser + '\'')
row = cursor.fetchone()

client = discord.Client()
disuser = row[0]

#helper class for an async timer
class Timer:
    def __init__(self, timeout, callback, context):
        self._timeout = timeout
        self._callback = callback
        self._context = context
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback(context)

    def cancel(self):
        self._task.cancel()

@client.event
async def on_ready():
    print('Logged in as: ' + client.user.name)
    bot_start = datetime.now()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    query = 'Select * from ' + database + commandtable + ' where \'' + message.content + '\' like COMMAND;'
    cursor.execute(query)
    row = cursor.fetchone()

    if row is None: return

    print(row)

    if not row[4] is None and not has_role(message.author, row[4]):
        await message.channel.send("User does not have sufficient permissions")
        return

    add_increment_to_queue(row[6], row[0])

    await process_command({'message': message, 'internal_cmd': row[2]})

    user_out = row[1]
    if len(message.mentions) > 0:
        for user in message.mentions:
            await message.channel.send(user_out.format(message, user))
    elif 'uptime' in row[2]:
        await message.channel.send(user_out.format(message, up_time))
    else:
        await message.channel.send(user_out.format(message))

    process_sql_writes()

@client.event
async def on_message_edit(before, after):
    print('no-op')

async def process_command(context):
    internal_cmd = context['internal_cmd']
    message = context['message']
    if internal_cmd is None: return

    #ex: timer 5 do assign Muted then remove Muted
    if 'timer' in internal_cmd:
        print('timer command')
        imediate_start = internal_cmd.find("do")
        timed_start = internal_cmd.find("then")
        delay = int(internal_cmd[5: immediate_start])
        if(imediate_start > timed_start):
            print('Improper order')
            return
        if(timed_start < 0 or imediate_start < 0):
            print('command missing input')
            return
        if(delay <= 0):
            print('bad delay')
            return
        immediate_cxt={'internal_cmd':internal_cmd[imediate_start + 2:timed_start], 'message':message}
        timed_cxt={'internal_cmd':internal_cmd[timed_start + 4:], 'message':message}
        await process_command(immediate_cxt)
        timer = Timer(delay, process_command, timed_cxt)

    if 'assign' in internal_cmd:
        await assign_user_role(list(message.mentions), get_role_by_name(internal_cmd[7:], message))

    elif 'remove' in internal_cmd:
        await del_user_role(list(message.mentions), get_role_by_name(internal_cmd[7:], message))

    elif 'uptime' in internal_cmd:
        up_time = datetime.now() - bot_start

    elif 'addcommand' in internal_cmd:

        sql_queue_out.put_nowait("")

    elif 'deletecommand' in internal_cmd:
        row = cursor.fetchone()
        while row:
            commandname = row[0]
            sql_queue_out.put("") # figure out delete query to run
            row = cursor.fetchone()

def add_increment_to_queue(previous_count, command_name):
    query = 'UPDATE ' + database + commandtable + ' set USES = ' + str(int(previous_count) + 1) + ' where COMMAND = \'' + command_name + '\''
    sql_queue_out.put(query)


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


def process_sql_writes():
    #print("sql queue size " + str(sql_queue_out.qsize()))
    while sql_queue_out.qsize() > 0:
        query = sql_queue_out.get()
        # print("writing query + \'" + query + "\'")
        cursor.execute(query)
        cnxn.commit()


client.run(disuser)

