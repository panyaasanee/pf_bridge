--[[
Quest.Var1=前置任務ID
Quest.Var2=系列任務ID
Quest.Var3=系列任務ID
Quest.Var4=系列任務ID
Quest.Var5=系列任務ID
Quest.Var6=系列任務ID
Quest.Var7=系列任務ID
Quest.Var8=系列任務ID
Quest.Var9=系列任務ID
Quest.Var10=系列任務ID
Quest.Var11=系列任務ID
Quest.Var12=還任務施放技能
Quest.Var13=任務開啟消失的怪物
Quest.Var14=任務開啟出現的怪物
Quest.Var15=任務回報消失的怪物
Quest.Var16=任務回報出現的怪物
Quest.Var17=任務開啟消失的怪物
Quest.Var18=任務開啟出現的怪物
Quest.Var19=任務回報消失的怪物
Quest.Var20=任務回報出現的怪物
--]]
function OpenAcceptUI_Run()
	
	movie = {}
	movie[1], movie[2] = string.find(Quest.StringVar1,"wmv")
	if movie[1] == nil then movie[1] = 0 end
	
	if movie[1] > 0 then
	
		Quest.PlayNPCMovie(Quest.StringVar1,1)
	else
	
		Mob.ShowAnimation(Quest.StringVar1)
	end
end 

function OpenReportUI_Run()

	movie = {}
	movie[1], movie[2] = string.find(Quest.StringVar2,"wmv")
	if movie[1] == nil then movie[1] = 0 end
	
	if movie[1] > 0 then
	
		Quest.PlayNPCMovie(Quest.StringVar2,1)
	else
	
		Mob.ShowAnimation(Quest.StringVar2)
	end
end 

function Check_Level()--任務等級檢查

	if (Quest.Var2 == 0) then--如果沒有設定接任務等級上限

		return 1
	elseif (Player.GetLv() <= Quest.Var2) then--角色等級小於接任務等級上
		
		return 1
	else
	
		return 0
	end
end

function Single_Mission_Check(Mission)

	if (Mission > 0) then
	
		if (Quest.GetQuestFlag(Mission) == Quest.Finish) then
		
			return 1
		else
		
			return 0
		end
	else
	
		return 1
	end
end

function Ex_Mission()--前置任務檢查
	
	if (Single_Mission_Check(Quest.Var1) == 1) then
	
		return 1
	else
	
		return 0
	end
end


--分隔線--
function Accept_Check()

	if (Check_Level() == 1 and Ex_Mission() == 1) then--如果符合接任務等級、前置任務已完成
 
		return 1
	else
	
		return 0
	end
   return 1; 
end

function Accept_Run()

    Quest.SetFlag(Quest.Active)--設定自身任務為進行中
	--↓設定系列任務進行中↓--
	if (Quest.Var2 > 0) then Quest.SetQuestFlag(Quest.Var2,1)
	if (Quest.Var3 > 0) then Quest.SetQuestFlag(Quest.Var3,1)
	if (Quest.Var4 > 0) then Quest.SetQuestFlag(Quest.Var4,1)
	if (Quest.Var5 > 0) then Quest.SetQuestFlag(Quest.Var5,1)
	if (Quest.Var6 > 0) then Quest.SetQuestFlag(Quest.Var6,1)
	if (Quest.Var7 > 0) then Quest.SetQuestFlag(Quest.Var7,1)
	if (Quest.Var8 > 0) then Quest.SetQuestFlag(Quest.Var8,1)
	if (Quest.Var9 > 0) then Quest.SetQuestFlag(Quest.Var9,1)
	if (Quest.Var10 > 0) then Quest.SetQuestFlag(Quest.Var10,1)
	if (Quest.Var11 > 0) then Quest.SetQuestFlag(Quest.Var11,1)
	--↑設定系列任務進行中↑--
	--↓設定NPC Appear↓--
	if (Quest.Var13 > 0 ) then Player.MobAppear(Quest.Var13, false) end
    if (Quest.Var14 > 0 ) then Player.MobAppear(Quest.Var14, true) end
    if (Quest.Var17 > 0 ) then Player.MobAppear(Quest.Var17, false) end
    if (Quest.Var18 > 0 ) then Player.MobAppear(Quest.Var18, true) end
	--↑設定NPC Appear↑--
    return 1;
end

function Report_Check() 
    
	local check_1 = Single_Mission_Check(Quest.Var2)
	local check_2 = Single_Mission_Check(Quest.Var3)
	local check_3 = Single_Mission_Check(Quest.Var4)
	local check_4 = Single_Mission_Check(Quest.Var5)
	local check_5 = Single_Mission_Check(Quest.Var6)
	local check_6 = Single_Mission_Check(Quest.Var7)
	local check_7 = Single_Mission_Check(Quest.Var8)
	local check_8 = Single_Mission_Check(Quest.Var9)
	local check_9 = Single_Mission_Check(Quest.Var10)
	local check_10 = Single_Mission_Check(Quest.Var11)
	
	if (check_1 * check_2 * check_3 * check_4 * check_5 * check_6 * check_7 * check_8 * check_9 * check_10 == 1) then
	
		return 1
	else
	
		return 0
	end
	return 1;
end

function Report_Run()
	
	if (Quest.Var12 > 0) then Player.CastSkillAt(Quest.Var12) end--還任務施放技能
	--↓設定NPC Appear↓--
	if (Quest.Var15 > 0 ) then Player.MobAppear(Quest.Var15, false) end
    if (Quest.Var16 > 0 ) then Player.MobAppear(Quest.Var16, true) end
    if (Quest.Var19 > 0 ) then Player.MobAppear(Quest.Var19, false) end
    if (Quest.Var20 > 0 ) then Player.MobAppear(Quest.Var20, true) end
	--↑設定NPC Appear↑--
	Mob.ShowAnimation(Quest.StringVar2)
	Quest.SetFlag(Quest.Finish)
	--↓發放任務獎勵↓--
    Quest.AddCriteriaExp()
    Quest.AddCriteriaSkillPoint()
    Quest.AddCriteriaCash()
	if (Quest.RewardItem1 > 0) then Player.AddItem(Quest.RewardItem1,Quest.RewardItemNum1) end
    if (Quest.RewardItem2 > 0) then Player.AddItem(Quest.RewardItem2,Quest.RewardItemNum2) end
    if (Quest.RewardItem3 > 0) then Player.AddItem(Quest.RewardItem3,Quest.RewardItemNum3) end
    if (Quest.RewardItem4 > 0) then Player.AddItem(Quest.RewardItem4,Quest.RewardItemNum4) end
    if (Quest.RewardItem5 > 0) then Player.AddItem(Quest.RewardItem5,Quest.RewardItemNum5) end
    if (Quest.RewardItem6 > 0) then Player.AddItem(Quest.RewardItem6,Quest.RewardItemNum6) end
    if (Quest.RewardChoose1 > 0) then Quest.RewardItemSelect(Quest.RewardChoose1,Quest.RewardChooseNum1) end
    if (Quest.RewardChoose2 > 0) then Quest.RewardItemSelect(Quest.RewardChoose2,Quest.RewardChooseNum2) end
    if (Quest.RewardChoose3 > 0) then Quest.RewardItemSelect(Quest.RewardChoose3,Quest.RewardChooseNum3) end
    if (Quest.RewardChoose4 > 0) then Quest.RewardItemSelect(Quest.RewardChoose4,Quest.RewardChooseNum4) end
    if (Quest.RewardChoose5 > 0) then Quest.RewardItemSelect(Quest.RewardChoose5,Quest.RewardChooseNum5) end
    if (Quest.RewardChoose6 > 0) then Quest.RewardItemSelect(Quest.RewardChoose6,Quest.RewardChooseNum6) end
	--↑發放任務獎勵↑--
	return 1;
end

function Delete_Run()

	--↓設定NPC Appear↓--
    if (Quest.Var13 > 0 ) then Player.MobAppear(Quest.Var13, true) end 
    if (Quest.Var14 > 0 ) then Player.MobAppear(Quest.Var14, false) end 
    if (Quest.Var17 > 0 ) then Player.MobAppear(Quest.Var17, true) end 
    if (Quest.Var18 > 0 ) then Player.MobAppear(Quest.Var18, false) end 
	--↑設定NPC Appear↑--
    return 1;
end