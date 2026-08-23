function OpenAcceptUI_Run()
    Quest.PlayNPCMovie(Quest.StringVar1,1)
end 

function OpenReportUI_Run()
    Mob.ShowAnimation(Quest.StringVar2)
end 

function Accept_Check()

   if( Quest.Var1 == 0) or
     ( Quest.GetQuestFlag(Quest.Var1) == Quest.Finish) then 
    return 1
	else
		return 0
	end 

   return 1;
end

function Accept_Run()
     
    Quest.SetFlag(Quest.Active)
	if (Quest.Var2 > 0 ) then Player.Teleport(Quest.Var2)
    end
	if Quest.Var3 > 0 then Player.OpenHelpUI(Quest.Var3)   -- 接任務開啟教學UI
	end
    if(Quest.Var11 > 0) then Mob.AddBuff(Quest.Var11,255)
    end
    if (Quest.Var13 > 0 ) then Player.MobAppear(Quest.Var13, false)
    end
    if (Quest.Var14 > 0 ) then Player.MobAppear(Quest.Var14, true)
    end
    if (Quest.Var17 > 0 ) then Player.MobAppear(Quest.Var17, false)
    end
    if (Quest.Var18 > 0 ) then Player.MobAppear(Quest.Var18, true)
    end
    return 1;
end


function Report_Check() 
 
        
    return 1;

end

function Report_Run()

    Mob.ShowAnimation(Quest.StringVar2)
    Quest.AddCriteriaExp()
    Quest.AddCriteriaSkillPoint()
    Quest.AddCriteriaCash()
	
	if Quest.GetQuestFlag(9000) ~= Quest.Finish then
	
		if   Player.GetClass() == 1  then 
		Player.AddAndEquip(2200206,8) 
		Player.AddAndEquip(2200206,16)
		end
		if  Player.GetClass() == 2 then 
		Player.AddAndEquip(2200406,8) 
		Player.AddAndEquip(2200606,16)
		end
		if   Player.GetClass() == 4  then Player.AddAndEquip(2201006,8) end
		if   Player.GetClass() == 8  then Player.AddAndEquip(2201410,8) end
		if   Player.GetClass() == 16 then Player.AddAndEquip(2200806,8) end
		if   Player.GetClass() == 32 then Player.AddAndEquip(2201206,8) end
	end
	
	if  Player.GetClass() == 1  then 
	
		Player.AddItem(Quest.RewardItem1,Quest.RewardItemNum1)
	elseif  Player.GetClass() == 2  then 
	
		Player.AddItem(Quest.RewardItem2,Quest.RewardItemNum2)
	elseif  Player.GetClass() == 4  then 
	
		Player.AddItem(Quest.RewardItem3,Quest.RewardItemNum3)
	elseif  Player.GetClass() == 8  then 
	
		Player.AddItem(Quest.RewardItem6,Quest.RewardItemNum6)
	elseif  Player.GetClass() == 16  then 
	
		Player.AddItem(Quest.RewardItem4,Quest.RewardItemNum4)
	elseif  Player.GetClass() == 32  then 
	
		Player.AddItem(Quest.RewardItem5,Quest.RewardItemNum5)
	end
    if Quest.Var4 > 0 then Player.OpenHelpUI(Quest.Var4)   -- 還任務開啟教學UI
	end
    if (Quest.RewardChoose1 > 0) then Quest.RewardItemSelect(Quest.RewardChoose1,Quest.RewardChooseNum1)
    end
    if (Quest.RewardChoose2 > 0) then Quest.RewardItemSelect(Quest.RewardChoose2,Quest.RewardChooseNum2)
    end
    if (Quest.RewardChoose3 > 0) then Quest.RewardItemSelect(Quest.RewardChoose3,Quest.RewardChooseNum3)
    end
    if (Quest.RewardChoose4 > 0) then Quest.RewardItemSelect(Quest.RewardChoose4,Quest.RewardChooseNum4)
    end
    if (Quest.RewardChoose5 > 0) then Quest.RewardItemSelect(Quest.RewardChoose5,Quest.RewardChooseNum5)
    end
    if (Quest.RewardChoose6 > 0) then Quest.RewardItemSelect(Quest.RewardChoose6,Quest.RewardChooseNum6)
    end
    if(Quest.Var12 > 0) then Mob.AddBuff(Quest.Var12,255)
    end
    if (Quest.Var15 > 0 ) then Player.MobAppear(Quest.Var15, false)
    end
    if (Quest.Var16 > 0 ) then Player.MobAppear(Quest.Var16, true)
    end
    if (Quest.Var19 > 0 ) then Player.MobAppear(Quest.Var19, false)
    end
    if (Quest.Var20 > 0 ) then Player.MobAppear(Quest.Var20, true)
    end    
    return 1;
end

function Delete_Run()
    Player.MobAppear(Quest.Var13, true)
    Player.MobAppear(Quest.Var14, false)
    Player.MobAppear(Quest.Var17, true)
    Player.MobAppear(Quest.Var18, false)
    return 1;
end
