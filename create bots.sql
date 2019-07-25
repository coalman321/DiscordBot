Drop table if exists Test.dbo.BotUsers

Create table Test.dbo.BotUsers (
BOTNAME varchar(255) not null, 
BOTKEY text not null,
Primary key (BOTNAME)
);

insert into Test.dbo.BotUsers values
('MODBOT', ''),
('ANOTHERUSER','');