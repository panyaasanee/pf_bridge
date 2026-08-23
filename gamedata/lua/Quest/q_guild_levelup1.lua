function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function OpenReportUI_Run()
    Mob.ShowAnimation(Quest.StringVar2)
end 

function Accept_Check()

   if (( Quest.Var1 == 0) or ( Quest.GetQuestFlag(Quest.Var1) == Quest.Finish)) and
      (( Quest.Var4 == 0) or ( Guild.CheckPlayerGuildJob(Quest.Var4))) and
      ( Guild.GetGuildLevel() == (Quest.Var6)) then 
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
      
    if ( Player.CheckItemNum(Quest.Var2,Quest.Var3)) then 

        return 1
	else
		return 0
	end 

   return 1;
end

function Report_Run()
    
    Mob.ShowAnimation(Quest.StringVar2)
    Quest.SetFlag(Quest.None)
    Player.RemoveItem(Quest.Var2,Quest.Var3)
    if ( Guild.GetGuildLevel() == (Quest.Var6)) then
    Guild.AddMeritExp(Quest.Var5)
    end

    return 1;
end

function Delete_Run()

    return 1;
end
