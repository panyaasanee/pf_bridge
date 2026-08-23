--[[
Quest.Var1=前置任務ID
Quest.Var2=任務等級上限
Quest.Var3=任務限時
Quest.Var4=互斥任務ID
Quest.Var5=殺怪ID 1
Quest.Var6=殺怪1數量
Quest.Var7=殺怪ID 2
Quest.Var8=殺怪2數量
Quest.Var9=指定技能ID
Quest.Var10=指定技能施放位置的X座標(還任務時)
Quest.Var11=Y座標
Quest.Var12=Z座標
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
    Mob.ShowAnimation(Quest.StringVar1)
end 

function OpenReportUI_Run()
    Mob.ShowAnimation(Quest.StringVar2)
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

function Ex_Mission()--前置任務檢查

	if (Quest.Var1 == 0) then--如果沒有設定前置任務
	
		return 1	
	else
	
		if (Quest.GetQuestFlag(Quest.Var1) == Quest.Finish) then --有設定前置任務的話，檢查前置是否已完成
		
			return 1
		else
		
			return 0
		end
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

	if (Quest.Var3 > 0) then Quest.CountDownTime(Quest.Var3) end --開啟任務計時器
	if (Quest.Var4 > 0) then Quest.SetQuestFlag(Quest.Var4,Quest.Finish) end --設定互斥任務
    Quest.SetFlag(Quest.Active)--設定自身任務為進行中
	if (Quest.Var5 > 0 and Quest.Var6 > 0) then Quest.MobKillCount(Quest.Var5,Quest.Var6) end
	if (Quest.Var7 > 0 and Quest.Var8 > 0) then Quest.MobKillCount(Quest.Var7,Quest.Var8) end
	
	--↓設定NPC Appear↓--
	if (Quest.Var13 > 0 ) then Player.MobAppear(Quest.Var13, false) end
    if (Quest.Var14 > 0 ) then Player.MobAppear(Quest.Var14, true) end
    if (Quest.Var17 > 0 ) then Player.MobAppear(Quest.Var17, false) end
    if (Quest.Var18 > 0 ) then Player.MobAppear(Quest.Var18, true) end
	--↑設定NPC Appear↑--
    return 1;
end

function Report_Check() 

    if Quest.Var9 > 0 then	Player.OutVehicle() end
	if (Quest.Var5 > 0 and Quest.Var6 > 0 and Quest.Var7 > 0 and Quest.Var8 > 0) then --2個計數器都有開的話
	
		if (Quest.CheckMobKillCount(Quest.Var5,Quest.Var6) and Quest.CheckMobKillCount(Quest.Var7,Quest.Var8)) then
		
			return 1
		else
		
			return 0
		end
	elseif (Quest.Var5 > 0 and Quest.Var6 > 0 and Quest.Var7 == 0 and Quest.Var8 == 0) then --只開1個計數器
	
		if (Quest.CheckMobKillCount(Quest.Var5,Quest.Var6)) then
		
			return 1
		else
		
			return 0
		end
	elseif (Quest.Var5 == 0 and Quest.Var6 == 0 and Quest.Var7 > 0 and Quest.Var8 > 0) then --只開1個計數器
	
		if (Quest.CheckMobKillCount(Quest.Var7,Quest.Var8)) then
		
			return 1
		else
		
			return 0
		end
	else
	
		return 1
	end
	return 1;
end

function Report_Run()
	
    if Quest.Var9 > 0 then Player.CastSkillXYZ(Quest.Var9,Quest.Var10,Quest.Var11,Quest.Var12) end--還任務施放技能
	--↓設定NPC Appear↓--
	if (Quest.Var15 > 0 ) then Player.MobAppear(Quest.Var15, false) end
    if (Quest.Var16 > 0 ) then Player.MobAppear(Quest.Var16, true) end
    if (Quest.Var19 > 0 ) then Player.MobAppear(Quest.Var19, false) end
    if (Quest.Var20 > 0 ) then Player.MobAppear(Quest.Var20, true) end
	--↑設定NPC Appear↑--
	Mob.ShowAnimation(Quest.StringVar2)
	--↓發放任務獎勵↓--
    Quest.AddCriteriaExp()
    Quest.AddCriteriaSkillPoint()
    Quest.AddCriteriaCash()
	Quest.SetFlag(Quest.Finish)
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