function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function OpenReportUI_Run()
    Mob.ShowAnimation(Quest.StringVar2)
end 

function Accept_Check()

   if(( Quest.Var1 == 0) or ( Quest.GetQuestFlag(Quest.Var1) == Quest.Finish) ) and
     ( Guild.CheckPlayerGuildJob(Quest.Var4) ) and
     ( Guild.GetGuildLevel() == (Quest.Var5)) then 
    return 1
	else
		return 0
	end 

   return 1;
end


function Accept_Run()
     
    Quest.SetFlag(Quest.Active)
    Quest.MobKillCount(Quest.Var6,Quest.Var7)
    Quest.MobKillCount(Quest.Var8,Quest.Var9)

    return 1;
end


function Report_Check() 
      
    if( (Quest.Var2==0) or (Player.CheckItemNum(Quest.Var2,Quest.Var3))) and
      ( (Quest.Var6==0) or (Quest.CheckMobKillCount(Quest.Var6,Quest.Var7)) ) and  
      ( (Quest.Var8==0) or (Quest.CheckMobKillCount(Quest.Var8,Quest.Var9)) ) then
        return 1
	else
		return 0
	end 

   return 1;
end

function Report_Run()

    Mob.ShowAnimation(Quest.StringVar2)
    Player.RemoveItem(Quest.Var2,Quest.Var3)
    Quest.SetFlag(Quest.None)
    Quest.SetQuestFlag(Quest.Var10,0)
    if ( Guild.GetGuildLevel() == (Quest.Var5)) then
    Guild.AddMeritExp(Quest.Var11)
    end

    return 1;
end

function Delete_Run()

    return 1;
end
