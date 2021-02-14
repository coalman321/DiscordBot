from queue import Queue
import time
import datetime
import discord
import pycouchdb
import asyncio
import re
import json

#global vars
bot_start = datetime.datetime.now()
up_time = datetime.timedelta()
client = discord.Client()

#connect to server
server = pycouchdb.Server("http://Tucker:Cole23tu@192.168.1.220:5984/")
print(server.info()["version"])
db = server.database("discordbot")

#get auth token for discord API
users = list(db.query("index/name", key="user"))
if(len(users) < 0): 
    print("error getting auth token from db")
    exit(-1)
user_token = db.get(users[0]["id"])["token"]
print(user_token)

#helper class for an async timer
class Timer:
    def __init__(self, timeout, callback, context):
        self._timeout = timeout
        self._callback = callback
        self._context = context
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        print("running callback")
        await self._callback(self._context)

    def cancel(self):
        self._task.cancel()

@client.event
async def on_ready():
    print("Logged in as: " + client.user.name)
    await client.change_presence(activity = discord.Streaming(name = "The good stuff", url = "https://www.youtube.com/watch?v=oHg5SJYRHA0%27"))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    def filtFunc(item):
        if(item["key"] is None): return False
        result = re.findall(item["key"], message.content)
        return len(result) > 0 and result[0] == message.content

    possible_matches = list(db.query("index/command"))
    if len(possible_matches) < 0: return
    matches = list(filter(filtFunc, possible_matches))
    if(len(matches) < 1): return

    cmd_doc = db.get(matches[0]["id"])
    if("role" in cmd_doc):
        has_valid_role = False
        for role in cmd_doc["role"]:
            has_valid_role |= has_role(message.author, cmd_doc["role"])
        if(not has_valid_role):
            await message.channel.send("User does not have sufficient permissions")
            return

    if("server" in cmd_doc and not message.guild.id == int(cmd_doc["server"])): 
        print(message.guild.id,  " ", cmd_doc["server"])
        print("command belongs to wrong server")
        return

    if("int_cmd" in cmd_doc): await process_command({"message":message, "cmd_doc":cmd_doc, "int_cmd":cmd_doc["int_cmd"]})
    if("reaction" in cmd_doc): await process_reaction(message, cmd_doc["reaction"])

    if("text" in cmd_doc): 
        user_out = cmd_doc["text"]
        if(len(message.mentions) > 0):
            for user in message.mentions:
                await message.channel.send(user_out.format(message, user))
        elif("int_cmd" in cmd_doc and "uptime" in cmd_doc["int_cmd"]):
            global up_time
            await message.channel.send(user_out.format(message, str(up_time).split(".", 2)[0]))
        else:
            await message.channel.send(user_out.format(message))

@client.event
async def on_message_edit(before, after):
    if(before.content == after.content): 
        return
    await process_reaction(after, "<:failbutton:501524918580805632>")

async def process_command(context):
    cmd_doc = context["cmd_doc"]
    int_cmd = context["int_cmd"]
    message = context["message"]

    #ex: timer 5 do assign Muted then remove Muted
    if("timer" in int_cmd):
        immediate_cxt={"int_cmd":cmd_doc["first_cmd"], "message":message, "cmd_doc": cmd_doc}
        timed_cxt={"int_cmd":cmd_doc["second_cmd"], "message":message, "cmd_doc": cmd_doc}
        await process_command(immediate_cxt)
        delay = int(message.content[len(cmd_doc["command"])-1: message.content.index("<")])
        print("delaying " + str(delay))
        timer = Timer(delay, process_command, timed_cxt)
        
    elif("for" in int_cmd):
        print("no-op for")

    if("assign" in int_cmd):
        await assign_user_role(list(message.mentions), get_role_by_name(int_cmd[7:], message))

    elif("remove" in int_cmd):
        await del_user_role(list(message.mentions), get_role_by_name(int_cmd[7:], message))

    elif("uptime" in int_cmd):
        global up_time
        up_time = datetime.datetime.now() - bot_start

    elif("debug" in int_cmd):
        #print(message)
        await message.channel.send(str(message))

async def process_reaction(message, reaction):
    if not reaction is None:
        await message.add_reaction(reaction)

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

client.run(user_token)