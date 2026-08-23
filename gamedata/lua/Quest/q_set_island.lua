--[[
Quest.Var1=前置任務ID
Quest.Var2=等級上限
Quest.Var3=前置登島任務ID
Quest.Var4=前置登島任務ID
Quest.Var5=前置登島任務ID
Quest.Var6=前置登島任務ID
Quest.Var7=前置登島任務ID
Quest.Var8=後續登島任務ID
Quest.Var9=後續登島任務ID
Quest.Var10=後續登島任務ID
Quest.Var11=後續登島任務ID
Quest.Var12=後續登島任務ID
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

	if Quest.Var2 == 0 then--如果沒有設定接任務等級上限

		return 1
	elseif Player.GetLv() <= Quest.Var2 then--角色等級小於接任務等級上
		
		return 1
	else
	
		return 0
	end
end

function Single_Mission_Check(Mission)

	if Mission > 0 then
	
		if Quest.GetQuestFlag(Mission) == Quest.Finish then
		
			return 1
		else
		
			return 0
		end
	else
	
		return 0 --這跟其他版型的Single_Mission_Check不同，因為後續邏輯為「至少有一個登島任務完成」就算通過所以必須用加法檢驗
	end
end

function Ex_Mission()--前置任務檢查
	
	if Quest.Var1 > 0 then
	
		if Quest.GetQuestFlag(Quest.Var1) == Quest.Finish then
		
			return 1
		else
		
			return 0
		end
	else
	
		return 1
	end
end

function Or_Mission()--前置登島任務

	check = {} --宣告check是一個Table
	check[1] = Single_Mission_Check(Quest.Var3)
	check[2] = Single_Mission_Check(Quest.Var4)
	check[3] = Single_Mission_Check(Quest.Var5)
	check[4] = Single_Mission_Check(Quest.Var6)
	check[5] = Single_Mission_Check(Quest.Var7)

	if check[1] + check[2] + check[3] + check[4] + check[5] > 0 then
	
		return 1
	else
	
		if Quest.Var3 == 0 and Quest.Var4 == 0 and Quest.Var5 == 0 and Quest.Var6 == 0 and Quest.Var7 == 0 then
		
			return 1
		else
		
			return 0
		end
	end
end

--分隔線--
function Accept_Check()

	if Check_Level() == 1 and Ex_Mission() == 1 and Or_Mission() == 1 and Quest.CanReportDailyQuest() then--如果符合接任務等級、前置任務、前置登島任務已完成
		
		return 1
	else
	
		return 0
	end
   return 1; 
end

function Accept_Run()
	myCheck = 0
	n_Mission = {} --宣告n_Mission是一個Table
	if Quest.Var8 > 0 then 
	
		myCheck = myCheck + 1
		n_Mission[myCheck] = Quest.Var8
	end
	if Quest.Var9 > 0 then 
	
		myCheck = myCheck + 1
		n_Mission[myCheck] = Quest.Var9
	end
	if Quest.Var10 > 0 then 
	
		myCheck = myCheck + 1
		n_Mission[myCheck] = Quest.Var10
	end
	if Quest.Var11 > 0 then 
	
		myCheck = myCheck + 1
		n_Mission[myCheck] = Quest.Var11
	end
	if Quest.Var12 > 0 then 
	
		myCheck = myCheck + 1
		n_Mission[myCheck] = Quest.Var12
	end
	
	if myCheck > 0 then --沒有設定登島任務的話就完全PASS
	
		math.randomseed(os.time()) --依照當前時間當作亂數種子
		
		for i = 1,2 do
		
			mySeed = math.random(myCheck) --值骰2次是因為隨機數種子是一樣的，所以會造成第一次值骰的結果也必定相同。所以忽略第一次的值骰結果..
		end
		Quest.SetQuestFlag(n_Mission[mySeed],1)--設定後續登島任務進行中
	end
	Quest.SetFlag(Quest.Active)--設定自身任務為進行中
	
	--↓設定NPC Appear↓--
	if Quest.Var13 > 0 then Player.MobAppear(Quest.Var13, false) end
    if Quest.Var14 > 0 then Player.MobAppear(Quest.Var14, true) end
    if Quest.Var17 > 0 then Player.MobAppear(Quest.Var17, false) end
    if Quest.Var18 > 0 then Player.MobAppear(Quest.Var18, true) end
	--↑設定NPC Appear↑--
    return 1;
end

function Report_Check() 
    
	return 1;
end

function Report_Run()
	
	--↓設定NPC Appear↓--
	if Quest.Var15 > 0 then Player.MobAppear(Quest.Var15, false) end
    if Quest.Var16 > 0 then Player.MobAppear(Quest.Var16, true) end
    if Quest.Var19 > 0 then Player.MobAppear(Quest.Var19, false) end
    if Quest.Var20 > 0 then Player.MobAppear(Quest.Var20, true) end
	--↑設定NPC Appear↑--
	Mob.ShowAnimation(Quest.StringVar2)
	Quest.ReportDailyQuest()
	Quest.SetFlag(Quest.None)
	--↓發放任務獎勵↓--
    Quest.AddCriteriaExp()
    Quest.AddCriteriaSkillPoint()
    Quest.AddCriteriaCash()
	if Quest.RewardItem1 > 0 then Player.AddItem(Quest.RewardItem1,Quest.RewardItemNum1) end
    if Quest.RewardItem2 > 0 then Player.AddItem(Quest.RewardItem2,Quest.RewardItemNum2) end
    if Quest.RewardItem3 > 0 then Player.AddItem(Quest.RewardItem3,Quest.RewardItemNum3) end
    if Quest.RewardItem4 > 0 then Player.AddItem(Quest.RewardItem4,Quest.RewardItemNum4) end
    if Quest.RewardItem5 > 0 then Player.AddItem(Quest.RewardItem5,Quest.RewardItemNum5) end
    if Quest.RewardItem6 > 0 then Player.AddItem(Quest.RewardItem6,Quest.RewardItemNum6) end
    if Quest.RewardChoose1 > 0 then Quest.RewardItemSelect(Quest.RewardChoose1,Quest.RewardChooseNum1) end
    if Quest.RewardChoose2 > 0 then Quest.RewardItemSelect(Quest.RewardChoose2,Quest.RewardChooseNum2) end
    if Quest.RewardChoose3 > 0 then Quest.RewardItemSelect(Quest.RewardChoose3,Quest.RewardChooseNum3) end
    if Quest.RewardChoose4 > 0 then Quest.RewardItemSelect(Quest.RewardChoose4,Quest.RewardChooseNum4) end
    if Quest.RewardChoose5 > 0 then Quest.RewardItemSelect(Quest.RewardChoose5,Quest.RewardChooseNum5) end
    if Quest.RewardChoose6 > 0 then Quest.RewardItemSelect(Quest.RewardChoose6,Quest.RewardChooseNum6) end
	--↑發放任務獎勵↑--
	return 1;
end

function Delete_Run()

	--↓設定NPC Appear↓--
    if Quest.Var13 > 0 then Player.MobAppear(Quest.Var13, true) end 
    if Quest.Var14 > 0 then Player.MobAppear(Quest.Var14, false) end 
    if Quest.Var17 > 0 then Player.MobAppear(Quest.Var17, true) end 
    if Quest.Var18 > 0 then Player.MobAppear(Quest.Var18, false) end 
	--↑設定NPC Appear↑--
    return 1;
end