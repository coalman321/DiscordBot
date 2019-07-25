Drop table if exists Test.dbo.BotCommands

Create table Test.dbo.BotCommands (
COMMAND varchar(255) not null, 
STRMESSAGE text not null,
INTCOMMAND varchar(255),
REACTION varchar(255),
PERMLEVEL varchar(255),
CASESENS bit not null,
USES bigint,
Primary Key (COMMAND)
);

insert into Test.dbo.BotCommands (COMMAND, STRMESSAGE, INTCOMMAND, REACTION, PERMLEVEL, CASESENS, USES)
	values
	('!brick%', '*hurriedly tosses a <:Brick:513528851729612819> in the general direction of {1.mention}*', null, null, null, 0, 0),
	('!example%', 'Ooh! Look a message!', null, null, null, 0, 0),
	('!mute%', '{1.mention} muted', 'assign Muted', null, 'Banhammers', 0, 0),
	('!nou%', 'Hey {1.mention}, <:nou:443600958983766028>!!!', null, null, null, 0, 0),
	('!ping%', 'pong', null, null, null, 0, 0),
	('!pong%', 'ping', null, null, null, 0, 0),
	('!ring%', 'Wrong!', null, null, null, 0, 0),
	('!unmute%', '{1.mention} un-muted', 'remove Muted', null, 'Banhammers', 0, 0),
	('%<:nou:443600958983766028>%', 'Hey {0.author.mention}, <:nou:443600958983766028>!!!', null, null, null, 0, 0),
	('%aaaaaaaa%', '<:What:504095033172033556>', null, null, null, 0, 0),
	('%am smart%', 'You are S M R T {0.author.mention}', null, null, null, 0, 0),
	('%good bot!%', 'Hooray!!! Im doing good things!', null, null, null, 0, 0),
	('%good bot?%', 'MEEEEEEEEE!!!! Im a good bot!', null, null, null, 0, 0),
	('%hahahahahahahahahahahahahahahahahahaha%', 'Whats so funny {0.author.mention}?', null, null, null, 0, 0),
	('%hehehehehehehehehehehehehehehehehehehe%', 'uhoh {0.author.mention} is being creepy', null, null, null, 0, 0),
	('%mouahaha%', 'Thar be evil afoot here!', null, null, null, 0, 0),
	('%ono%', 'oh heck', null, null, null, 0, 0),
	('%ready for this?', '<:Rede:505912136346632192>', null, null, null, 0, 0),
	('%yeet%', 'yeets a <:Brick:513528851729612819> for {0.author.mention}', null, null, null, 0, 0),
	('!reload%', 'I am V3, I do not need to reload', null, null, 'Banhammers', 0, 0)