--[[
Quest.Var1=前置任務ID
Quest.Var2=任務等級上限
Quest.Var3=傳送方式            
Quest.Var4=位置

傳送方式                         位置
0=單人傳位置(完成時傳送)         MarkerID
1=多人傳位置(完成時傳送)         MarkerID
2=單人傳副本(完成時傳送)         副本ID
3=多人傳副本(完成時傳送)         副本群組ID
4=單人傳位置(接任時傳送)         MarkerID
5=多人傳位置(接任時傳送)         MarkerID
6=單人傳副本(接任時傳送)         副本ID
7=多人傳副本(接任時傳送)         副本群組ID

功能組1
Quest.Var5=功能類型  1=扣除道具  2=施放技能  3=施放Buff  4=護衛模式
Quest.Var6=參數1       道具ID      技能ID      BuffID      MobID
Quest.Var7=參數2       道具數量                Buff等級    護衛時限
功能組2
Quest.Var8=同上
Quest.Var9=同上
Quest.Var10=同上

Quest.Var11=要播放的影片ID(影片只支援單人傳送)
Quest.Var12=
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

function Dim()

	myType = {}
	mySet_1 = {}
	mySet_2 = {}
	myType[1] = Quest.Var5
	mySet_1[1] = Quest.Var6
	mySet_2[1] = Quest.Var7
	myType[2] = Quest.Var8
	mySet_1[2] = Quest.Var9
	mySet_2[2] = Quest.Var10
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

function CheckNum(ItemID, ItemNum, Type)

	if Type == 0 then
	
		if ItemID > 0 and ItemNum > 0 and Player.CheckItemNum(ItemID,ItemNum) then

			return 1
		else

			return 0
		end
	elseif Type == 1 then
	
		if ItemID > 0 and ItemNum > 0 and Party.CheckPartyItem(ItemID,ItemNum) then

			return 1
		else

			return 0
		end
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

	Dim()

	for i = 1,2 do
	
		if myType[i] == 4 then
		
			if mySet_2[i] > 0 then 
			
				Mob.StartMove(mySet_2[i])
				Quest.CountDownTime(mySet_2[i])
			end
		end
	end

	if Quest.Var3 == 4 then
	
		if Quest.Var11 == 0 then--有設定影片的話就播放影片
		
			if Quest.Var4 > 0 then Player.Teleport(Quest.Var4) end
		else
		
			if Quest.Var4 > 0 then Player.TeleportThenPlayMovie(Quest.Var4,Quest.Var11) end
		end
		Quest.SetFlag(Quest.None)--接任務就傳送，傳完就把任務設定為None
	elseif Quest.Var3 == 5 then
	
		if Quest.Var4 > 0 then Player.TeleportWithVehicle(Quest.Var4) end
		Quest.SetFlag(Quest.None)
	elseif Quest.Var3 == 6 then
	
		if Quest.Var11 == 0 then--有設定影片的話就播放影片
		
			if Quest.Var4 > 0 then Player.EnterInstance(Quest.Var4) end
		else
		
			if Quest.Var4 > 0 then Player.EnterInstanceThenPlayMovie(Quest.Var4,Quest.Var11) end
		end
		Quest.SetFlag(Quest.None)
	elseif Quest.Var3 == 7 then
	
		if Quest.Var4 > 0 then Player.LoadInstanceGroup(Quest.Var4) end
		Quest.SetFlag(Quest.None)
	else
	
		Quest.SetFlag(Quest.Active)--設定自身任務為進行中
	end
	
	--↓設定NPC Appear↓--
	if (Quest.Var13 > 0 ) then Player.MobAppear(Quest.Var13, false) end
    if (Quest.Var14 > 0 ) then Player.MobAppear(Quest.Var14, true) end
    if (Quest.Var17 > 0 ) then Player.MobAppear(Quest.Var17, false) end
    if (Quest.Var18 > 0 ) then Player.MobAppear(Quest.Var18, true) end
	--↑設定NPC Appear↑--
    return 1;
end

function Report_Check() 	

	Dim()
	myCheck = 1--初始化
	for i = 1,2 do
	
		if myType[i] == 1 then
		
			if Quest.Var3 == 0 or Quest.Var3 == 2 then
			
				myCheck = myCheck * CheckNum(mySet_1[i], mySet_2[i], 0)
			elseif Quest.Var3 == 1 or Quest.Var3 == 3 then
			
				myCheck = myCheck * CheckNum(mySet_1[i], mySet_2[i], 1)
			end
		elseif myType[i] == 4 then
		
			if Mob.CheckApproachTarget() then
			
				myCheck = myCheck * 1--這樣乘法方式，只要功能組1或2任意一個未達成，myCheck就會等於0
			else
			
				myCheck = myCheck * 0
			end
		end
	end
	
	if Quest.Var3 >=4 and Quest.Var3 <=7 then myCheck = 0 end
	
	--最後在迴圈外只要檢查myCheck是不是0就知道有沒有滿足可回報的條件了
	if myCheck == 0 then
	
		return 0
	else
	
		return 1
	end
	return 1;
end

function Report_Run()
	
	--↓設定傳送方式↓--
	if Quest.Var3 == 0 then
	
		if Quest.Var11 == 0 then--有設定影片的話就播放影片
		
			if Quest.Var4 > 0 then Player.Teleport(Quest.Var4) end
		else
		
			if Quest.Var4 > 0 then Player.TeleportThenPlayMovie(Quest.Var4,Quest.Var11) end
		end
	elseif Quest.Var3 == 1 then
	
		if Quest.Var4 > 0 then Player.TeleportWithVehicle(Quest.Var4) end
	elseif Quest.Var3 == 2 then
	
		if Quest.Var11 == 0 then--有設定影片的話就播放影片
		
			if Quest.Var4 > 0 then Player.EnterInstance(Quest.Var4) end
		else
		
			if Quest.Var4 > 0 then Player.EnterInstanceThenPlayMovie(Quest.Var4,Quest.Var11) end
		end
	elseif Quest.Var3 == 3 then
	
		if Quest.Var4 > 0 then Player.LoadInstanceGroup(Quest.Var4) end
	end
	--↑設定傳送方式↑--
	--↓設定功能群組1↓--
	
	for i = 1,2 do
	
		if myType[i] == 1 then--扣除道具
		
			if Quest.Var3 == 0 or Quest.Var3 == 2 then
			
				if CheckItemNum(mySet_1[i],mySet_2[i],0) == 1 then Player.RemoveItem(mySet_1[i],mySet_2[i]) end
			elseif Quest.Var3 == 1 or Quest.Var3 == 3 then
			
				if CheckItemNum(mySet_1[i],mySet_2[i],1) == 1 then Party.RemovePartyItem(mySet_1[i],mySet_2[i]) end
			end
		elseif myType[i] == 2 then--施放技能
		
			if mySet_1[i] > 0 then Player.CastSkillAt(mySet_1[i]) end
		elseif myType[i] == 3 then--施放Buff
		
			if mySet_1[i] > 0 and mySet_2[i] > 0 then Player.AddBuff(mySet_1[i],mySet_2[i]) end
		end
	end
	--↑設定功能群組1↑--
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

	for i = 1,2 do
	
		if myType[i] == 4 then--NPC歸位
		
			if mySet_1[i] > 0 then Mob.EndMove(mySet_1[i]) end
		end
	end

	--↓設定NPC Appear↓--
    if (Quest.Var13 > 0 ) then Player.MobAppear(Quest.Var13, true) end 
    if (Quest.Var14 > 0 ) then Player.MobAppear(Quest.Var14, false) end 
    if (Quest.Var17 > 0 ) then Player.MobAppear(Quest.Var17, true) end 
    if (Quest.Var18 > 0 ) then Player.MobAppear(Quest.Var18, false) end 
	--↑設定NPC Appear↑--
    return 1;
end