--[[
Quest.Var1=前置任務ID
Quest.Var2=戰場ID
Quest.Var3=可接陣營(0=海軍, 1=海盜)

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

		if myDay ~= 3 and Guild.GetPVPFaction() == Quest.Var3 then--週三沒有海戰可以報名

			return 1
		
		end
	
	end
	return 0
	
end

function Accept_Run()

	if Player.CheckBuff(9903) then
	
		Player.ShowMessage(897)--有疲勞Buff時無法報名海戰
	
	else

		if Quest.CheckOpenTime(1930,1955) or 
		Quest.CheckOpenTime(2030,2055) or 
		Quest.CheckOpenTime(2130,2155) or 
		Quest.CheckOpenTime(2230,2255) or
		Quest.CheckOpenTime(2330,2355) or
		Quest.CheckOpenTime(0030,0055) or
		Quest.CheckOpenTime(0130,0155) then
		
			Player.BookBattleField(Quest.Var2)
			
		else  --PCCINT-47608修正不顯示訊息 PCCINT-47800修正回顯示訊息
		
			Player.ShowMessage(890)--不在報名時間內不可報名
			
		end
		
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