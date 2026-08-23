function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
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
    
    return 1;
end


function Report_Check() 

    if (Quest.Var2 == 0 or Player.CheckAchievement(Quest.Var2))  and
       (Quest.Var3 == 0 or Player.CheckAchievement(Quest.Var3))  and
      ( Quest.Var4 == 0 or Player.CheckAchievement(Quest.Var4)) and
      ( Quest.Var5 == 0 or Player.CheckAchievement(Quest.Var5)) then
 
    return 1
	else
	return 0
    end 
        
    return 1;
end

function Report_Run()
    Mob.ShowAnimation(Quest.StringVar2)
    Quest.AddCriteriaExp()
    Quest.AddCriteriaSkillPoint()
    Quest.AddCriteriaCash()
    if Quest.Var6 > 0 then Player.OpenHelpUI(Quest.Var6) end
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
    return 1
end

function Delete_Run()
    
    return 1;
end
