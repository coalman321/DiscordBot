Select * from Test.dbo.BotCommands
where '!pong' like concat('%', STRCOMMAND, '%')