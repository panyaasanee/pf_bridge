function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function OpenReportUI_Run()
    Mob.ShowAnimation(Quest.StringVar2)
end

function Accept_Check()

    if ( Player.GetClass() ~= (Quest.Var2)) and 
       ( Player.GetPpClass() == 0 ) and 
       ( Quest.GetQuestFlag(Quest.Var10) == Quest.None ) and
       ( Quest.GetQuestFlag(Quest.Var11) == Quest.None ) and
       ( Quest.GetQuestFlag(Quest.Var12) == Quest.None ) and
       ( Quest.GetQuestFlag(Quest.Var13) == Quest.None ) and
       ( Quest.GetQuestFlag(Quest.Var14) == Quest.None ) and
       (( Quest.GetQuestFlag(Quest.Var1) == Quest.Finish ) or
       ( Quest.GetQuestFlag(Quest.Var5) == Quest.Finish ) or
       ( Quest.GetQuestFlag(Quest.Var6) == Quest.Finish ) or
       ( Quest.GetQuestFlag(Quest.Var7) == Quest.Finish ) or
       ( Quest.GetQuestFlag(Quest.Var8) == Quest.Finish ) or
       ( Quest.GetQuestFlag(Quest.Var9) == Quest.Finish ))then

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
      
    if( Player.GetCash() >= (Quest.Var3) ) then
        return 1
	else
		return 0
	end 

   return 1;
end

function Report_Run()

    Mob.ShowAnimation(Quest.StringVar2)
    Player.AddPpClass(Quest.Var2)
	Quest.SetFlag(Quest.None)
    Player.AddCash(Quest.Var4)
    Quest.AddCriteriaExp()
    Quest.AddCriteriaSkillPoint()
      
    return 1;
end

function Delete_Run()

    return 1;
end
