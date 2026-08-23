function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function OpenReportUI_Run()
    Mob.ShowAnimation(Quest.StringVar2)
end 

function Accept_Check()
    if( Quest.CheckOpenTime(Quest.Var3,Quest.Var4) == true ) then
        return 1
	else
		return 0
	end

   return 1;
end

function Accept_Run()
   Party.SignUpArena()

   return 0;
end



function Report_Check()

   return 1;
end

function Report_Run()
 
    return 1;
end

function Delete_Run()
    Player.MobAppear(Quest.Var13, true)
    Player.MobAppear(Quest.Var14, false)
    Player.MobAppear(Quest.Var17, true)
    Player.MobAppear(Quest.Var18, false)
    return 1;
end
