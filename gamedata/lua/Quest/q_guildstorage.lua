function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function Accept_Check()

    if( Player.CheckGuild() == true )and
	(( Quest.Var1 == 0) or ( Quest.GetQuestFlag (Quest.Var1) == Quest.Finish)) and
	( Guild.GetGuildLevel() >= (Quest.Var2) ) then 
    return 1
	else
		return 0
	end 

   return 1;
end


function Accept_Run()
     
    Guild.OpenGuildStorage()
    Quest.SetFlag(Quest.None)
    return 1;
end


function Report_Check() 
 
    if( Quest.GetFlag() == Quest.Active) then 
    return 1
	else
		return 0
	end 

   return 1;
end

function Report_Run()

    
    return 1;
end


function Delete_Run()
	return 1;
end
