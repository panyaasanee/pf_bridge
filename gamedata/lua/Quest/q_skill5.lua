function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
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
    Player.OpenUI("Skill_Learn2")
    Quest.AddCriteriaExp()
    Quest.AddCriteriaSkillPoint()
    Quest.AddCriteriaCash()
    if (  Player.GetClass() == 1 ) then 
          Player.AddItem(Quest.RewardItem1,Quest.RewardItemNum1)  
	end
    if (  Player.GetClass() == 2 ) then 
          Player.AddItem(Quest.RewardItem2,Quest.RewardItemNum2) 
	end
    if (  Player.GetClass() == 4 ) then 
          Player.AddItem(Quest.RewardItem3,Quest.RewardItemNum3)
	end
    if (  Player.GetClass() == 16 ) then 
          Player.AddItem(Quest.RewardItem4,Quest.RewardItemNum4) 
	end
    if (  Player.GetClass() == 32 ) then 
          Player.AddItem(Quest.RewardItem5,Quest.RewardItemNum5) 
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
