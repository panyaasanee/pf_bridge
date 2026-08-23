function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function Accept_Check()
    
    if ( Player.CheckGuild() == false ) and
	(( Quest.Var1 == 0) or ( Quest.GetQuestFlag(Quest.Var1) == Quest.Finish) )then 
    return 1
	else
		return 0
	end 

   return 1;
end


function Accept_Run()
    
	if Quest.Var4 > 0 then Player.OpenHelpUI(Quest.Var4) end
    Player.OpenUI("Guild_Set")
    Quest.SetFlag(Quest.None)
    return 0
	
end


function Report_Check() 

   return 0
   
end


function Report_Run()
   
    return 0
	
end


function Delete_Run()

	return 1
	
end
