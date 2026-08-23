--[[
Quest.Var1=前置任務ID
Quest.Var2=接任務日期
Quest.Var3=回收海戰徽章數量
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

		if Quest.CanReportDailyQuest() then
	
			myDay = Quest.GetWeekDay()--今天星期幾

			if myDay == Quest.Var2 then

				return 1

			end
			
		end
	
	end
	return 0
	
end

function Accept_Run()

	Quest.SetFlag(Quest.Active)
	return 1
	
end

function Report_Check() 

	if Player.CheckItemNum(2600392,Quest.Var3) then 
	
		return 1
		
	end
	
	return 0
end

function Report_Run()

	Quest.SetFlag(Quest.None)
	Mob.ShowAnimation(Quest.StringVar2)
	--↓發放任務獎勵↓--
    Quest.AddLvCriteriaExp()
	Quest.AddLvCriteriaSkillPoint()
	Player.RemoveItem(2600392,Quest.Var3)
	Quest.ReportDailyQuest()
	return 1
	
end

function Delete_Run()

	return 1
	
end