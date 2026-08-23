function OpenReportUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function OpenReportUI_Run()
    Mob.ShowAnimation(Quest.StringVar2)
end 

function Accept_Check()

    if ( Player.CheckGuild() == true )and
       (( Quest.Var1 == 0) or ( Quest.GetQuestFlag(Quest.Var1) == Quest.Finish)) and
	   ( Guild.CheckPlayerGuildJob(Quest.Var4) ) and
       (( Quest.Var9 == 0 ) or ( Guild.GetGuildLevel() >= (Quest.Var9))) then
        return 1
	else
		return 0
	end 

   return 1;
end

function Accept_Run()
     
    Quest.SetFlag(Quest.Active)
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
	if (Player.CheckItemNum(Quest.Var2,Quest.Var3))and
	   (Player.GetCash() >= (Quest.Var5)) then
	    return 1
	else
		return 0
	end 

   return 1;
end

function Report_Run()

    Mob.ShowAnimation(Quest.StringVar2)
    Player.RemoveItem(Quest.Var2,Quest.Var3)
    Quest.AddLvCriteriaExp()
    Quest.AddLvCriteriaSkillPoint() 
    Quest.AddLvCriteriaCash() 
    Quest.SetFlag(Quest.None)
    Player.AddCash(Quest.Var8)
	if(Quest.Var6 > 0) then Mob.CallMob(Quest.Var6,Quest.Var7)  
	end
	if (Quest.RewardItem1 > 0) then Player.AddItem(Quest.RewardItem1,Quest.RewardItemNum1)
    end
    if (Quest.RewardItem2 > 0) then Player.AddItem(Quest.RewardItem2,Quest.RewardItemNum2)
    end
    if (Quest.RewardItem3 > 0) then Player.AddItem(Quest.RewardItem3,Quest.RewardItemNum3)
    end
    if (Quest.RewardItem4 > 0) then Player.AddItem(Quest.RewardItem4,Quest.RewardItemNum4)
    end
    if (Quest.RewardItem5 > 0) then Player.AddItem(Quest.RewardItem5,Quest.RewardItemNum5)
    end
    if (Quest.RewardItem6 > 0) then Player.AddItem(Quest.RewardItem6,Quest.RewardItemNum6)
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
