--[[
Quest.Var1=前置任務ID
Quest.Var2=任務等級上限
Quest.Var3=任務計時器, 0=不開啟, 不等於0就是秒數
Quest.Var4=是否設定為不打滿就可回報, 0=要打滿才能回報, 1=不打滿就可以回報
Quest.Var5=要殺的怪物1 ID
Quest.Var6=要殺的怪物1 數量
Quest.Var7=要殺的怪物2 ID
Quest.Var8=要殺的怪物2 數量
Quest.Var9=要殺的怪物3 ID
Quest.Var10=要殺的怪物3 數量
Quest.Var11=要殺的怪物4 ID
Quest.Var12=要殺的怪物4 數量
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

function Count_MobKillCount()--檢查到底開了幾個計數器

	if (Quest.Var5 > 0 and Quest.Var6 > 0 and Quest.Var7 == 0 and Quest.Var8 == 0 and 
	Quest.Var9 == 0 and Quest.Var10 == 0 and Quest.Var11 == 0 and Quest.Var12 == 0)then --如果開了1個殺怪計數器
	
		return 1
		
	elseif (Quest.Var5 > 0 and Quest.Var6 > 0 and Quest.Var7 > 0 and Quest.Var8 > 0 and 
	Quest.Var9 == 0 and Quest.Var10 == 0 and Quest.Var11 == 0 and Quest.Var12 == 0) then --如果開了2個殺怪計數器
	
		return 2
		
	elseif (Quest.Var5 > 0 and Quest.Var6 > 0 and Quest.Var7 > 0 and Quest.Var8 > 0 and 
	Quest.Var9 > 0 and Quest.Var10 > 0 and Quest.Var11 == 0 and Quest.Var12 == 0) then --如果開了3個殺怪計數器
	
		return 3
		
	elseif (Quest.Var5 > 0 and Quest.Var6 > 0 and Quest.Var7 > 0 and Quest.Var8 > 0 and 
	Quest.Var9 > 0 and Quest.Var10 > 0 and Quest.Var11 > 0 and Quest.Var12 > 0) then --如果開了4個殺怪計數器
	
		return 4
	else
	
		return 1
	end
end

function Kill_Percentage(CountNumber)--計算平均殺怪的百分比

	if (CountNumber == 1) then
	
		myPercentage = math.floor(Quest.GetMobKillCount(Quest.Var5) * 100 / Quest.Var6)
	elseif (CountNumber == 2) then
	
		myPercentage = math.floor((
		(Quest.GetMobKillCount(Mob1) * 100 / Quest.Var6)+
		(Quest.GetMobKillCount(Mob2) * 100 / Quest.Var8)
		) /CountNumber)
	elseif (CountNumber == 3) then
	
		myPercentage = math.floor((
		(Quest.GetMobKillCount(Mob1) * 100 / Quest.Var6)+
		(Quest.GetMobKillCount(Mob2) * 100 / Quest.Var8)+
		(Quest.GetMobKillCount(Mob3) * 100 / Quest.Var10)
		) /CountNumber)
	elseif (CountNumber == 4) then
	
		myPercentage = math.floor((
		(Quest.GetMobKillCount(Mob1) * 100 / Quest.Var6)+
		(Quest.GetMobKillCount(Mob2) * 100 / Quest.Var8)+
		(Quest.GetMobKillCount(Mob3) * 100 / Quest.Var10)+
		(Quest.GetMobKillCount(Mob4) * 100 / Quest.Var12)
		) /CountNumber)
	end
	return myPercentage
end

--分隔線--
function Accept_Check()

	if (Check_Level() == 1 and Ex_Mission() == 1 and Quest.CanReportDailyQuest()) then--如果符合接任務等級、前置任務已完成以及每日任務可回報
 
		return 1
	else
	
		return 0
	end
   return 1; 
end

function Accept_Run()

	if (Quest.Var3 > 0) then Quest.CountDownTime(Quest.Var3) end --開啟任務計時器
    if (Quest.Var5 > 0 and Quest.Var6 > 0) then Quest.MobKillCount(Quest.Var5,Quest.Var6) end --開啟殺怪1計數器
	if (Quest.Var7 > 0 and Quest.Var8 > 0) then Quest.MobKillCount(Quest.Var7,Quest.Var8) end --開啟殺怪2計數器
	if (Quest.Var9 > 0 and Quest.Var10 > 0) then Quest.MobKillCount(Quest.Var9,Quest.Var10) end --開啟殺怪3計數器
	if (Quest.Var11 > 0 and Quest.Var12 > 0) then Quest.MobKillCount(Quest.Var11,Quest.Var12) end --開啟殺怪4計數器
    Quest.SetFlag(Quest.Active)--設定任務為進行中
	if (Quest.Var13 > 0 ) then Player.MobAppear(Quest.Var13, false) end--設定NPC Appear
    if (Quest.Var14 > 0 ) then Player.MobAppear(Quest.Var14, true) end--設定NPC Appear
    if (Quest.Var17 > 0 ) then Player.MobAppear(Quest.Var17, false) end--設定NPC Appear
    if (Quest.Var18 > 0 ) then Player.MobAppear(Quest.Var18, true) end--設定NPC Appear
    return 1;
end

function Report_Check() 
    
	CM = Count_MobKillCount()--先找出開了幾個計數器
	if (Quest.Var4 == 1) then--如果是設定為各殺一隻就能回報
	
		if (CM == 1) then--根據開啟幾個計數器判斷做不同的檢查
		
			if (Quest.GetMobKillCount(Quest.Var5) > 0) then 
			
				return 1 
			else

				return 0
			end
		elseif (CM == 2) then
		
			if (Quest.GetMobKillCount(Quest.Var5) > 0 and Quest.GetMobKillCount(Quest.Var7) > 0) then 
			
				return 1 
			else
			
				return 0
			end
		elseif (CM == 3) then
		
			if (Quest.GetMobKillCount(Quest.Var5) > 0 and Quest.GetMobKillCount(Quest.Var7) > 0 and 
			Quest.GetMobKillCount(Quest.Var9) > 0) then 
			
				return 1 
			else
			
				return 0
			end
		elseif (CM == 4) then
		
			if (Quest.GetMobKillCount(Quest.Var5) > 0 and Quest.GetMobKillCount(Quest.Var7) > 0 and 
			Quest.GetMobKillCount(Quest.Var9) > 0 and Quest.GetMobKillCount(Quest.Var11) > 0) then 
			
				return 1 
			else

				return 0
			end
		end
	else--只要Quest.Var不是設定為1就是預設為打滿才能回報
	
		if (CM == 1) then--根據開啟幾個計數器判斷做不同的檢查
		
			if (Quest.CheckMobKillCount(Quest.Var5,Quest.Var6)) then 
			
				return 1 
			else

				return 0
			end
		elseif (CM == 2) then
		
			if (Quest.CheckMobKillCount(Quest.Var5,Quest.Var6) and Quest.CheckMobKillCount(Quest.Var7,Quest.Var8)) then
			
				return 1 
			else

				return 0
			end
		elseif (CM == 3) then
		
			if (Quest.CheckMobKillCount(Quest.Var5,Quest.Var6) and Quest.CheckMobKillCount(Quest.Var7,Quest.Var8) and 
			Quest.CheckMobKillCount(Quest.Var9,Quest.Var10)) then 
			
				return 1 
			else

				return 0
			end
		elseif (CM == 4) then
		
			if (Quest.CheckMobKillCount(Quest.Var5,Quest.Var6) and Quest.CheckMobKillCount(Quest.Var7,Quest.Var8) and 
			Quest.CheckMobKillCount(Quest.Var9,Quest.Var10) and Quest.CheckMobKillCount(Quest.Var11,Quest.Var12)) then 
			
				return 1 
			else

				return 0
			end
		end
	end
	return 1;
end

function Report_Run()

	CM = Count_MobKillCount()--先找出開了幾個計數器
	KP = Kill_Percentage(CM)--計算殺怪百分比
	
	--開始根據百分比分配獎勵
	if (KP >= 0 and KP <= 33) then--完全沒殺的獎勵
	
		if (Quest.RewardItem1 > 0) then Player.AddItem(Quest.RewardItem1,Quest.RewardItemNum1) end
		
	elseif (KP > 33 and KP <=66) then
	
		if (Quest.RewardItem1 > 0) then Player.AddItem(Quest.RewardItem1,Quest.RewardItemNum1) end
		if (Quest.RewardItem2 > 0) then Player.AddItem(Quest.RewardItem2,Quest.RewardItemNum2) end
		
	elseif (KP > 66 and KP < 100) then
	
		if (Quest.RewardItem1 > 0) then Player.AddItem(Quest.RewardItem1,Quest.RewardItemNum1) end
		if (Quest.RewardItem2 > 0) then Player.AddItem(Quest.RewardItem2,Quest.RewardItemNum2) end
		if (Quest.RewardItem3 > 0) then Player.AddItem(Quest.RewardItem3,Quest.RewardItemNum3) end
		if (Quest.RewardItem4 > 0) then Player.AddItem(Quest.RewardItem4,Quest.RewardItemNum4) end
		if (Quest.RewardChoose1 > 0) then Quest.RewardItemSelect(Quest.RewardChoose1,Quest.RewardChooseNum1) end
		if (Quest.RewardChoose2 > 0) then Quest.RewardItemSelect(Quest.RewardChoose2,Quest.RewardChooseNum2) end
		if (Quest.RewardChoose3 > 0) then Quest.RewardItemSelect(Quest.RewardChoose3,Quest.RewardChooseNum3) end
		
	elseif (KP == 100) then
	
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
	end
	
	--任務結束處理
	if (Quest.Var15 > 0 ) then Player.MobAppear(Quest.Var15, false) end--設定NPC Appear
    if (Quest.Var16 > 0 ) then Player.MobAppear(Quest.Var16, true) end--設定NPC Appear
    if (Quest.Var19 > 0 ) then Player.MobAppear(Quest.Var19, false) end--設定NPC Appear
    if (Quest.Var20 > 0 ) then Player.MobAppear(Quest.Var20, true) end--設定NPC Appear
	Mob.ShowAnimation(Quest.StringVar2)
	Quest.ReportDailyQuest()
	Quest.AddLvCriteriaExp()
	Quest.AddLvCriteriaSkillPoint() 
    Quest.AddLvCriteriaCash() 
	Quest.SetFlag(Quest.None)
	return 1;
end

function Delete_Run()
    if (Quest.Var13 > 0 ) then Player.MobAppear(Quest.Var13, true) end --設定NPC Appear
    if (Quest.Var14 > 0 ) then Player.MobAppear(Quest.Var14, false) end --設定NPC Appear
    if (Quest.Var17 > 0 ) then Player.MobAppear(Quest.Var17, true) end --設定NPC Appear
    if (Quest.Var18 > 0 ) then Player.MobAppear(Quest.Var18, false) end --設定NPC Appear
    return 1;
end