function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function OpenReportUI_Run()
    Mob.ShowAnimation(Quest.StringVar2)
end 

function Accept_Check()

   if Player.CheckGuild() and 
   (( Quest.Var1 == 0) or ( Quest.GetQuestFlag (Quest.Var1) == Quest.Finish)) and
   Quest.CheckGuildOfflineQuest() then 
		return 1
	else
		return 0
	end 

   return 1;
end

function Accept_Run()
     
    Quest.MobKillCount(Quest.Var4,Quest.Var5)
	Quest.MobKillCount(Quest.Var6,Quest.Var7)
	Quest.MobKillCount(Quest.Var8,Quest.Var9)
	Player.CastSkillAt(Quest.Var3)
	Quest.StartGuildOfflineQuest()
    Quest.SetFlag(Quest.Active)
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
       
    if( Quest.CheckMobKillCount(Quest.Var4,Quest.Var5) and 
	   Quest.CheckMobKillCount(Quest.Var6,Quest.Var7) and
	   Quest.CheckMobKillCount(Quest.Var8,Quest.Var9)) then
	  
        return 1
	else
		return 0
	end 

   return 1;
end

function Report_Run()
    Mob.ShowAnimation(Quest.StringVar2)
	Quest.ReportGuildOfflineQuest()
    Quest.SetFlag(Quest.None)
	Quest.AddCriteriaExp()
    Quest.AddCriteriaSkillPoint()
    Quest.AddCriteriaCash()
    if (Quest.Var15 > 0 ) then Player.MobAppear(Quest.Var15, false)
    end
    if (Quest.Var16 > 0 ) then Player.MobAppear(Quest.Var16, true)
    end
    if (Quest.Var19 > 0 ) then Player.MobAppear(Quest.Var19, false)
    end
    if (Quest.Var20 > 0 ) then Player.MobAppear(Quest.Var20, true)
    end    	
	if (Quest.Var10 > 0) then Player.CastSkillAt(Quest.Var10)
	end
	if (Quest.Var11 > 0) then Guild.AddMeritExp(Quest.Var11)
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