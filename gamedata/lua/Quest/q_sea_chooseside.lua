--[[
Quest.Var1=前置任務ID
Quest.Var2=陣營(0=海軍, 1=海盜)

--]]


--分隔線--

function OpenAcceptUI_Run()
	
	movie = {}
	movie[1], movie[2] = string.find(Quest.StringVar1,"wmv")--movie[1]會接到W這個字的位置，movie[2]會接到v這個字的位置
	if movie[1] == nil then 
	
		movie[1] = 0 
		
	end
	
	if movie[1] > 0 then
	
		Quest.PlayNPCMovie(Quest.StringVar1,1)
		
	else
	
		Mob.ShowAnimation(Quest.StringVar1)
		
	end
	
end 

function OpenReportUI_Run()

	movie = {}
	movie[1], movie[2] = string.find(Quest.StringVar2,"wmv")--movie[1]會接到W這個字的位置，movie[2]會接到v這個字的位置
	if movie[1] == nil then 
	
		movie[1] = 0 
		
	end
	
	if movie[1] > 0 then
	
		Quest.PlayNPCMovie(Quest.StringVar2,1)
		
	else
	
		Mob.ShowAnimation(Quest.StringVar2)
		
	end
	
end 

function Accept_Check()

	if Quest.Var1 == 0 or Quest.GetQuestFlag(Quest.Var1) == Quest.Finish then--檢查前置任務

		myDay = Quest.GetWeekDay()--今天星期幾
		myRank = Player.GetGuildRank()--玩家的公會會階

		if myDay == 3 and myRank == 4 then--只有會長在週三才可以接任務

			return 1
			
		end
	
	end
	return 0
	
end

function Accept_Run()

	if Guild.GetPVPFaction() ~= Quest.Var2 then --避免重複設定陣營
	
		Guild.SetPVPFaction(Quest.Var2)
	
	end
	Quest.SetFlag(Quest.None)
	return 1
	
end

function Report_Check() 

	return 0

end

function Report_Run()
	
	return 1
	
end

function Delete_Run()

	return 1
	
end