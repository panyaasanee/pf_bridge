function OpenAcceptUI_Run()
    Quest.PlayNPCMovie(Quest.StringVar1,1)
end 

function OpenReportUI_Run()
    Quest.PlayNPCMovie(Quest.StringVar1,1)
end 

function Accept_Check()

	if( Quest.Var1 == 0 or Quest.GetQuestFlag(Quest.Var1) == Quest.Finish) and
      ( Quest.GetQuestFlag(Quest.Var2) == Quest.None) then
        return 1
	else
		return 0
	end 

   return 1;
end


function Accept_Run()
     
    Player.OpenUI("Skill_Learn2")
    Quest.SetFlag(Quest.None)
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
 
    if( Quest.GetFlag() == Quest.Active) then 
    return 1
	else
		return 0
	end 

   return 1;
end

function Report_Run()

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
