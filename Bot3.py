import discord
import pyodbc


server = 'localhost'
database = 'Test'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes;')
cursor = cnxn.cursor()

#Sample select query
cursor.execute("SELECT @@version;")
row = cursor.fetchone()
while row:
    print(row[0])
    row = cursor.fetchone()

'''Select * from Test.dbo.BotCommands
where '!pong' like concat('%', STRCOMMAND, '%')''' #query for commands

# Sample insert query
cursor.execute("INSERT SalesLT.Product (Name, ProductNumber, StandardCost, ListPrice, SellStartDate) OUTPUT INSERTED.ProductID VALUES ('SQL Server Express New 20', 'SQLEXPRESS New 20', 0, 0, CURRENT_TIMESTAMP )")
row = cursor.fetchone()

while row:
    print('Inserted Product key is ' + str(row[0]))
    row = cursor.fetchone()

client = discord.Client()
disuser = 1 #grab bot token from DB




@client.event
async def on_ready():
    print('Logged in as: ' + client.user.name)

@client.event
async def on_message(message):
    if message.author == client.user:
        return



@client.event
async def on_message_edit(before, after):
    print('no-op')


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


async def assign_user_role(user, role):
    await user.add_roles(role)


async def del_user_role(user, role):
    await user.remove_roles(role)

#client.run(disuser)