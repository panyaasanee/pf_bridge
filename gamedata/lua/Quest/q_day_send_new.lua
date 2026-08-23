--[[
Quest.Var1=前置任務ID
Quest.Var2=任務等級上限
Quest.Var3=任務限時
Quest.Var4=快遞道具ID
Quest.Var5=回報道具1 ID
Quest.Var6=回報道具1數量
Quest.Var7=回報道具1是否扣除 0=要扣, 1=不扣(不扣除就可以做出「要先殺怪或偷取證件偽裝成XX人員，然後再送有加料的貨物給對方」這種電影常見的橋段。)
Quest.Var8=回報道具2 ID
Quest.Var9=回報道具2數量
Quest.Var10=回報道具2是否扣除 0=要扣, 1=不扣 (送貨物沒有在回收證件的...)
Quest.Var11=接任務時施放技能1
Quest.Var12=還任務時施放技能1
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

	if (Check_Level() == 1 and Ex_Mission() == 1 and Quest.CanReportDailyQuest()) then--如果符合接任務等級、前置任務已完成
 
		return 1
	else
	
		return 0
	end
   return 1; 
end

function Accept_Run()

	if (Quest.Var3 > 0) then Quest.CountDownTime(Quest.Var3) end --開啟任務計時器
    Quest.SetFlag(Quest.Active)--設定自身任務為進行中
	if (Quest.Var4 > 0) then Player.AddItem(Quest.Var4,1) end--接任務給予道具(寫死只給1個道具，這裡可以用包裝帶過，所以不給企畫做數量設定。Ex:5個蘋果可以包裝為一箱水果...)
	if (Quest.Var11 > 0) then Player.CastSkillAt(Quest.Var11) end--接任務施放技能
	--↓設定NPC Appear↓--
	if (Quest.Var13 > 0 ) then Player.MobAppear(Quest.Var13, false) end
    if (Quest.Var14 > 0 ) then Player.MobAppear(Quest.Var14, true) end
    if (Quest.Var17 > 0 ) then Player.MobAppear(Quest.Var17, false) end
    if (Quest.Var18 > 0 ) then Player.MobAppear(Quest.Var18, true) end
	--↑設定NPC Appear↑--
    return 1;
end

function Report_Check() 
    
	if (Quest.Var4 > 0) then--Var4是NPC交待的物品，所以一定要有
	
		if (Quest.Var5 > 0 and Quest.Var8 > 0) then--檢查附加物品
		
			if (Player.CheckItemNum(Quest.Var5,Quest.Var6) and Player.CheckItemNum(Quest.Var8,Quest.Var9)) then
			
				return 1
			else
			
				return 0
			end
		elseif (Quest.Var5 > 0 and Quest.Var8 == 0) then
		
			if (Player.CheckItemNum(Quest.Var5,Quest.Var6)) then
			
				return 1
			else
			
				return 0
			end	
		elseif (Quest.Var5 == 0 and Quest.Var8 > 0)
		
			if (Player.CheckItemNum(Quest.Var8,Quest.Var9)) then
			
				return 1
			else
			
				return 0
			end	
		else
		
			return 1--沒設定要檢查其他道具的話，就直接給過了
		end
	else
	
		return 0
	end
	return 1;
end

function Report_Run()
	
	--↓回收道具↓--
	if (Player.CheckItemNum(Quest.Var4,1)) then Player.RemoveItem(Quest.Var4,1) end
	if (Player.CheckItemNum(Quest.Var5,Quest.Var6) and Quest.Var7 == 0) then Player.RemoveItem(Quest.Var5,Quest.Var6) end
	if (Player.CheckItemNum(Quest.Var8,Quest.Var9) and Quest.Var10 == 0) then Player.RemoveItem(Quest.Var8,Quest.Var9) end
	--↑回收道具↑--
	if (Quest.Var12 > 0) then Player.CastSkillAt(Quest.Var12) end--還任務施放技能
	--↓設定NPC Appear↓--
	if (Quest.Var15 > 0 ) then Player.MobAppear(Quest.Var15, false) end
    if (Quest.Var16 > 0 ) then Player.MobAppear(Quest.Var16, true) end
    if (Quest.Var19 > 0 ) then Player.MobAppear(Quest.Var19, false) end
    if (Quest.Var20 > 0 ) then Player.MobAppear(Quest.Var20, true) end
	--↑設定NPC Appear↑--
	Mob.ShowAnimation(Quest.StringVar2)
	Quest.SetFlag(Quest.None)
	Quest.ReportDailyQuest()
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

	delItem = {}--宣告delItem是Table
	delItem[1] = Player.GetItemNum(Quest.Var4)
	if delItem[1] > 0 then Player.RemoveItem(Quest.Var4,delItem[1]) end
	delItem[2] = Player.GetItemNum(Quest.Var5)
	if delItem[2] > 0 and Quest.Var7 == 0 then Player.RemoveItem(Quest.Var5,delItem[2]) end
	delItem[3] = Player.GetItemNum(Quest.Var8)
	if delItem[3] > 0 and Quest.Var10 == 0 then Player.RemoveItem(Quest.Var8,delItem[3]) end
	
	--↓設定NPC Appear↓--
    if (Quest.Var13 > 0 ) then Player.MobAppear(Quest.Var13, true) end 
    if (Quest.Var14 > 0 ) then Player.MobAppear(Quest.Var14, false) end 
    if (Quest.Var17 > 0 ) then Player.MobAppear(Quest.Var17, true) end 
    if (Quest.Var18 > 0 ) then Player.MobAppear(Quest.Var18, false) end 
	--↑設定NPC Appear↑--
    return 1;
end