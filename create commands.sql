Drop table if exists Test.dbo.BotCommands

Create table Test.dbo.BotCommands (
STRCOMMAND varchar(255) not null, 
STRMESSAGE text not null,
INTCOMMAND varchar(255),
REACTION varchar(255),
PERMLEVEL varchar(255),
CASESENS bit not null,
USES bigint,
Primary Key (STRCOMMAND)
);

insert into Test.dbo.BotCommands (STRCOMMAND, STRMESSAGE, INTCOMMAND, REACTION, PERMLEVEL, CASESENS, USES)
	values
	('!ping', 'pong', null, null, null, 0, 0),
	('!pong', 'ping', null, null, null, 0, 0),
	('yeet', 'yeets a <:Brick:513528851729612819> for {0.author.mention}', null, null, null, 0, 0)
	--('', '', null, null, null, 0, 0),
	--('', '', null, null, null, 0, 0),
	--('', '', null, null, null, 0, 0),
	--('', '', null, null, null, 0, 0)
