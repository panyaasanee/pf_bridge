--[[
Quest.Var1=前置任務ID
Quest.Var2=任務等級上限
Quest.Var3=任務限時

功能組1
Quest.Var4=功能類型
Quest.Var5=功能參數1
Quest.Var6=功能參數2

功能組2
Quest.Var7=
Quest.Var8=
Quest.Var9=

功能組3
Quest.Var10=
Quest.Var11=
Quest.Var12=

功能類型索引                功能參數1       功能參數2
0=沒事
1=接任務時設定任務旗標      任務ID          旗標值
2=完成時設定任務旗標        任務ID          旗標值
3=接任務放技能              技能ID          
4=還任務放技能              技能ID			
5=接任務放角色Buff          BuffID          Buff等級
6=還任務放角色Buff          BuffID          Buff等級
7=接任務播歌曲              0=廣播,1=不廣播 (採用此類型時NPC動作會只吃StringVar1, StringVar2被設定為歌曲名稱)
8=完成任務播歌曲            0=廣播,1=不廣播 (採用此類型時NPC動作會只吃StringVar1, StringVar2被設定為歌曲名稱)
9=完成後傳送                MarkerID        影片ID
10=完成後進副本             副本ID          影片ID
11=NPC語音(OpenUI)          語音ID
12=NPC語音(接任務)          語音ID
13=NPC語音(ReportUI)        語音ID
14=NPC語音(完成任務)        語音ID
15=完成時撥放影片           影片ID
16=接任務開始護衛           NPC重置秒數
17=檢查前置任務             任務ID          旗標值
18=特殊前置任務             任務ID(此任務旗標為0 or 2都滿足可接條件)
19=設定完成條件檢查Buff     BuffID          0=有此Buff滿足可回報條件, 1= 無此Buff滿足可回報條件
20=接任務時開教學UI         UIID
21=還任務時開教學UI         UIID
22=接任務時開啟配置區       配置區ID
23=接任務開啟殺怪計數器     怪物ID          怪物數量
24=接任務開啟道具計數器     道具ID          道具數量
25=快遞類型道具計數器       道具ID          道具數量
26=完成任務時道具放快捷列   道具ID          第幾個快捷列與第幾格的數字(Ex:109是第1個快捷列的第9格)
27=接任務時調整鏡頭方向     方向(時鐘方位表示法1~12)
28=接任務時播放動作(採用此類型時NPC動作會只吃StringVar1, StringVar2被設定為接任務時播放的動作)
29=接任務的時間條件         星期幾(0=週日，1=週一....)
30=接任務的陣營限制         陣營(0=海軍，1=海盜)


Quest.Var13=任務開啟消失的怪物
Quest.Var14=任務開啟出現的怪物
Quest.Var15=任務回報消失的怪物
Quest.Var16=任務回報出現的怪物
Quest.Var17=任務開啟消失的怪物
Quest.Var18=任務開啟出現的怪物
Quest.Var19=任務回報消失的怪物
Quest.Var20=任務回報出現的怪物
--]]

function Dim()

	funcCount = 3 --總共幾個功能組
	myType = {}
	mySet_1 = {}
	mySet_2 = {}
	myType[1] = Quest.Var4
	mySet_1[1] = Quest.Var5
	mySet_2[1] = Quest.Var6
	myType[2] = Quest.Var7
	mySet_1[2] = Quest.Var8
	mySet_2[2] = Quest.Var9
	myType[3] = Quest.Var10
	mySet_1[3] = Quest.Var11
	mySet_2[3] = Quest.Var12
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

	Dim()
	exCheck={}
	for i = 1,funcCount do

		if myType[i] == 17 then

			if Quest.GetQuestFlag(mySet_1[i]) == mySet_2[i] then --滿足設定條件就return 1
			
				exCheck[i] = 1
				
			else
			
				exCheck[i] = 0
				
			end
			
		elseif myType[i] == 18 then
		
			if Quest.GetQuestFlag(mySet_1[i]) == 0 or Quest.GetQuestFlag(mySet_1[i]) == 2 then --滿足設定條件就return 1
			
				exCheck[i] = 1
				
			else
			
				exCheck[i] = 0
				
			end	
			
		else
		
			exCheck[i] = 1
			
		end
	end
	
	if (Quest.Var1 == 0) then--如果沒有設定前置任務
	
		exCheck[funcCount + 1] = 1	
		
	else
	
		if (Quest.GetQuestFlag(Quest.Var1) == Quest.Finish) then --有設定前置任務的話，檢查前置是否已完成
		
			exCheck[funcCount + 1] = 1
			
		else
		
			exCheck[funcCount + 1] = 0
			
		end
		
	end
	
	exFinal = 1
	for i = 1,funcCount + 1 do
	
		exFinal = exFinal * exCheck[i]

	end
	
	if exFinal == 1 then
	
		return 1
		
	else
	
		return 0
		
	end
end

--分隔線--

function OpenAcceptUI_Run()
	
	Dim()
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
	for i = 1,funcCount do
	
		if myType[i] == 11 then --播放NPC語音
		
			Quest.PlayNPCVoice(mySet_1[i]) 
			
		end 
		
	end
end 

function OpenReportUI_Run()

	QuestString = Quest.StringVar2
	movie = {}
	Dim()
	for i = 1,funcCount do
	
		if myType[i] == 7 or myType[i] == 8 or myType[i] == 28 then--判斷是否為使用Quest.StringVar1
		
			QuestString = Quest.StringVar1
			
		elseif myType[i] == 13 then--播放NPC語音
		
			Quest.PlayNPCVoice(mySet_1[i])
			
		end
	end
	
	movie[1], movie[2] = string.find(QuestString,"wmv")
	if movie[1] == nil then 
	
		movie[1] = 0 
	
	end
	
	if movie[1] > 0 then
			
		Quest.PlayNPCMovie(QuestString,1)
		
	else
			
		Mob.ShowAnimation(QuestString)
		
	end
end 

function Accept_Check()

    Dim()
	acpCheck={}
	for i = 1,funcCount do
	
	    if myType[i] == 5 or myType[i] == 6 then--是否為給Buff
			
			if Player.CheckBuff(mySet_1[i]) then--檢查身上是否有Buff
				
				acpCheck[i] = 0
				
			else
				
				acpCheck[i] = 1
				
			end
			
		elseif myType[i] == 29 then--日期條件
		
			if Quest.GetWeekDay() == mySet_1[i] then
			
				acpCheck[i] = 1
				
			else
			
				acpCheck[i] = 0
			
			end
		
		elseif myType[i] == 30 then--陣營條件
		
			if Guild.GetPVPFaction() == mySet_1[i] then
				
				acpCheck[i] = 1
				
			else
			
				acpCheck[i] = 0
			
			end
			
		else
		
			acpCheck[i] = 1
			
		end   
	end

	if (Check_Level() == 1 and Ex_Mission() == 1) then--如果符合接任務等級、前置任務已完成
 
		acpCheck[funcCount + 1] = 1
		
	else
	
		acpCheck[funcCount + 1] = 0
		
	end

	acpFinal = 1
	for i = 1,funcCount + 1 do
	
		acpFinal = acpFinal * acpCheck[i]

	end
	
	if acpFinal == 1 then
	
		return 1
		
	else
	
		return 0
		
	end
end

function Accept_Run()

	Dim()

	if (Quest.Var3 > 0) then --開啟任務計時器
	
		Quest.CountDownTime(Quest.Var3) 
		
	end 
	
	Quest.SetFlag(Quest.Active)--設定自身任務為進行中
	
	for i = 1,funcCount do
	
		if myType[i] == 1 then--設定任務旗標
		
			if mySet_1[i] > 0 then 
			
				Quest.SetQuestFlag(mySet_1[i],mySet_2[i]) 
			
			end
			
		elseif myType[i] == 3 then--接任務施放技能
		
			if mySet_1[i] > 0 then 
			
				Player.CastSkillAt(mySet_1[i]) 
				
			end
			Player.OutVehicle()
			
		elseif myType[i] == 5 then--接任務施放Buff
		
			if mySet_1[i] > 0 and mySet_2[i] > 0 then 
			
				Player.AddBuff(mySet_1[i],mySet_2[i]) 
				
			end
			
			Player.OutVehicle()
			
		elseif myType[i] == 7 then--播放歌曲
		
			Scene.ChangeMainMusic(Quest.StringVar2,mySet_1[i])
			
		elseif myType[i] == 12 then--播放NPC語音
		
			if mySet_1[i] > 0 then 
			
				Quest.PlayNPCVoice(mySet_1[i]) 
				
			end
		elseif myType[i] == 16 then--護衛
		
			if mySet_1[i] > 0 then 
			
				Mob.StartMove(mySet_1[i]) 
				
			end
			
		elseif myType[i] == 20 then--開啟教學UI
		
			if mySet_1[i] > 0 then 
			
				Player.OpenHelpUI(mySet_1[i]) 
				
			end
			
		elseif myType[i] == 22 then--開啟配置區
		
			if mySet_1[i] > 0 then 
			
				Scene.PlacementON(mySet_1[i]) 
			
			end
			
		elseif myType[i] == 23 then--開啟怪物計數器
		
			if mySet_1[i] > 0 and mySet_2[i] > 0 then 
			
				Quest.MobKillCount(mySet_1[i],mySet_2[i]) 
				
			end
			
		elseif myType[i] == 25 then--增加道具數量
		
			if mySet_1[i] > 0 and mySet_2[i] > 0 then 
			
				Player.AddItem(mySet_1[i],mySet_2[i]) 
				
			end
			
		elseif myType[i] == 27 then--調整鏡頭方向
		
			if mySet_1[i] > 0 then 
			
				Player.CameraFocus(mySet_1[i]) 
				
			end
			
		elseif myType[i] == 28 then--NPC做動作
		
			Mob.ShowAnimation(Quest.StringVar2)	
			
		end
	end
	--↓設定NPC Appear↓--
	if (Quest.Var13 > 0 ) then 
	
		Player.MobAppear(Quest.Var13, false) 
	
	end
    if (Quest.Var14 > 0 ) then 
	
		Player.MobAppear(Quest.Var14, true) 
		
	end
    if (Quest.Var17 > 0 ) then 
	
		Player.MobAppear(Quest.Var17, false) 
	
	end
    if (Quest.Var18 > 0 ) then 
	
		Player.MobAppear(Quest.Var18, true) 
		
	end
	--↑設定NPC Appear↑--
	return 1
end

function Report_Check() 

    Dim()
	myCheck={}
	for i = 1,funcCount do
	
	    if myType[i] == 16 then--是否為護衛任務
		
		    if  Mob.CheckApproachTarget() then
		   
				myCheck[i] = 1
				
	        else
		   
	            myCheck[i] = 0
				
	        end
			
		elseif myType[i] == 19 then--檢查完成條件Buff
			
			if mySet_2[i] == 0 then--設定為0表示有此Buff為可回報
			
				if Player.CheckBuff(mySet_1[i]) then
				
					myCheck[i] = 1
					
				else
				
					myCheck[i] = 0
					
				end
				
			elseif mySet_2[i] == 1 then--設定為1表示無此Buff為可回報
			
				if Player.CheckBuff(mySet_1[i]) then
				
					myCheck[i] = 0
					
				else
				
					myCheck[i] = 1
					
				end			
			end
			
		elseif myType[i] == 23 then--檢查怪物計數器
		
			if Quest.CheckMobKillCount(mySet_1[i],mySet_2[i]) then 
			
				myCheck[i] = 1
				
			else
			
				myCheck[i] = 0
				
			end
			
		elseif myType[i] == 24 or myType[i] == 25 then--檢查道具計數器
		
			if Player.CheckItemNum(mySet_1[i],mySet_2[i]) then 
			
				myCheck[i] = 1
				
			else
			
				myCheck[i] = 0
				
			end
			
		else
		
			myCheck[i] = 1
			
		end   
	end
	
	myFinal = 1
	for i = 1,funcCount do
	
		myFinal = myFinal * myCheck[i]

	end
	
	if myFinal == 1 then
	
		return 1
		
	else
	
		return 0
		
	end
end

function Report_Run()
	
	Dim()
	Quest.SetFlag(Quest.None)
	Mob.ShowAnimation(Quest.StringVar2)
	--↓發放任務獎勵↓--
    Quest.AddCriteriaExp()
    Quest.AddCriteriaSkillPoint()
    Quest.AddCriteriaCash()
	if (Quest.RewardItem1 > 0) then 
	
		Player.AddItem(Quest.RewardItem1,Quest.RewardItemNum1) 
		
	end
    
	if (Quest.RewardItem2 > 0) then 
	
		Player.AddItem(Quest.RewardItem2,Quest.RewardItemNum2) 
		
	end
    
	if (Quest.RewardItem3 > 0) then 
	
		Player.AddItem(Quest.RewardItem3,Quest.RewardItemNum3) 
		
	end
	
    if (Quest.RewardItem4 > 0) then 
	
		Player.AddItem(Quest.RewardItem4,Quest.RewardItemNum4) 
		
	end
	
    if (Quest.RewardItem5 > 0) then 
	
		Player.AddItem(Quest.RewardItem5,Quest.RewardItemNum5) 
		
	end
	
    if (Quest.RewardItem6 > 0) then 
	
		Player.AddItem(Quest.RewardItem6,Quest.RewardItemNum6) 
		
	end
	
    if (Quest.RewardChoose1 > 0) then 
	
		Quest.RewardItemSelect(Quest.RewardChoose1,Quest.RewardChooseNum1) 
		
	end
	
    if (Quest.RewardChoose2 > 0) then 
	
		Quest.RewardItemSelect(Quest.RewardChoose2,Quest.RewardChooseNum2) 
		
	end
	
    if (Quest.RewardChoose3 > 0) then 
	
		Quest.RewardItemSelect(Quest.RewardChoose3,Quest.RewardChooseNum3) 
		
	end
	
    if (Quest.RewardChoose4 > 0) then 
	
		Quest.RewardItemSelect(Quest.RewardChoose4,Quest.RewardChooseNum4) 
		
	end
	
    if (Quest.RewardChoose5 > 0) then 
	
		Quest.RewardItemSelect(Quest.RewardChoose5,Quest.RewardChooseNum5) 
		
	end
	
    if (Quest.RewardChoose6 > 0) then 
	
		Quest.RewardItemSelect(Quest.RewardChoose6,Quest.RewardChooseNum6) 
		
	end
	--↑發放任務獎勵↑--
	
	for i = 1,funcCount do
	
		if myType[i] == 2 then--設定任務旗標
		
			if mySet_1[i] > 0 then 
			
				Quest.SetQuestFlag(mySet_1[i],mySet_2[i]) 
				
			end
			
		elseif myType[i] == 4 then--還任務施放技能
		
			if mySet_1[i] > 0 then 
			
				Player.CastSkillAt(mySet_1[i]) 
				
			end
			
			Player.OutVehicle()
			
		elseif myType[i] == 6 then--還任務施放Buff
		
			if mySet_1[i] > 0 and mySet_2[i] > 0 then 
			
				Player.AddBuff(mySet_1[i],mySet_2[i]) 
				
			end
			
			Player.OutVehicle()
			
		elseif myType[i] == 8 then--播放歌曲
		
			Scene.ChangeMainMusic(Quest.StringVar2,mySet_1[i])
			
		elseif myType[i] == 9 then--傳座標點
		
			if mySet_2[i] > 0 then--檢查要不要播影片
			
				if mySet_1[i] > 0 then 
				
					Player.TeleportThenPlayMovie(mySet_1[i],mySet_2[i]) 
					
				end
				
			else
			
				if mySet_1[i] > 0 then 
				
					Player.Teleport(mySet_1[i]) 
					
				end
				
			end
		elseif myType[i] == 10 then--傳進副本
		
			if mySet_2[i] > 0 then--檢查要不要播影片
			
				if mySet_1[i] > 0 then 
				
					Player.EnterInstanceThenPlayMovie(mySet_1[i],mySet_2[i]) 
					
				end
			else
			
				if mySet_1[i] > 0 then 
				
					Player.EnterInstance(mySet_1[i]) 
					
				end
			end
			
		elseif myType[i] == 14 then--播放NPC語音
		
			Quest.PlayNPCVoice(mySet_1[i])
			
		elseif myType[i] == 15 then--撥放影片
		
			Player.PlayMovie(mySet_1[i])
			
		elseif myType[i] == 16 then--護衛任務
		
			if mySet_2[i] == 0 then 
			
				Mob.EndMove(mySet_1[i]) 
				
			end
			
		elseif myType[i] == 21 then--開啟教學UI
		
			if mySet_1[i] > 0 then 
			
				Player.OpenHelpUI(mySet_1[i]) 
			
			end
			
		elseif myType[i] == 24 or myType[i] == 25 then--扣除道具
		
			if mySet_1[i] > 0 and mySet_2[i] > 0 then 
			
				Player.RemoveItem(mySet_1[i],mySet_2[i]) 
				
			end
			
		elseif myType[i] == 26 then--道具放快捷列
			
			if mySet_1[i] > 0 and mySet_2[i] > 0 then
			
				itemPlace = {}
				itemPlace[1] = math.floor(mySet_2[i] * 0.01)--拆解出3位數中的第1個數字（表示第幾個快捷列）
				itemPlace[2] = math.mod(mySet_2[i],100)--拆解出後2個數字（表示快捷列上的第幾格）
				Player.ItemAddon(mySet_1[i],itemPlace[1],itemPlace[2])
				
			end
		end
	end
	
	--↓設定NPC Appear↓--
	if (Quest.Var15 > 0 ) then 
	
		Player.MobAppear(Quest.Var15, false) 
	
	end
    if (Quest.Var16 > 0 ) then 
	
		Player.MobAppear(Quest.Var16, true) 
		
	end
    if (Quest.Var19 > 0 ) then 
	
		Player.MobAppear(Quest.Var19, false) 
		
	end
    if (Quest.Var20 > 0 ) then 
	
		Player.MobAppear(Quest.Var20, true) 
		
	end
	--↑設定NPC Appear↑--
	return 1
end

function Delete_Run()

	Dim()
	for i = 1,funcCount do
	
		if myType[i] == 16 then --護衛任務取消
		
			if mySet_1[i] > 0 then 
			
				Mob.EndMove(mySet_1[i]) 
			
			end
			
		elseif myType[i] == 24 or myType[i] == 25 then--扣除道具
		
			if mySet_1[i] > 0 and mySet_2[i] > 0 then 
			
				Player.RemoveItem(mySet_1[i],mySet_2[i]) 
				
			end
			
		end
	end
	--↓設定NPC Appear↓--
    if (Quest.Var13 > 0 ) then 
	
		Player.MobAppear(Quest.Var13, true) 
		
	end 
	
    if (Quest.Var14 > 0 ) then 
	
		Player.MobAppear(Quest.Var14, false) 
	
	end 
	
    if (Quest.Var17 > 0 ) then 
	
		Player.MobAppear(Quest.Var17, true) 
		
	end 
	
    if (Quest.Var18 > 0 ) then 
	
		Player.MobAppear(Quest.Var18, false) 
		
	end 
	--↑設定NPC Appear↑--
	return 1
end