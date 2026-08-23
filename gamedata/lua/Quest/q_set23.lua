function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function OpenReportUI_Run()
    Mob.ShowAnimation(Quest.StringVar2)
end 

function Accept_Check()

   if ((Quest.Var1 == 0 or Quest.GetQuestFlag(Quest.Var1) == Quest.Finish) and
	  (Quest.Var2 == 0 or Quest.GetQuestFlag(Quest.Var2) == Quest.Active) and
	  (Quest.Var5 == 0 or Player.CheckItemNum(Quest.Var5,Quest.Var1))) then
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
 
    if ((Quest.Var3)==0 or Player.CheckItemNum(Quest.Var3,Quest.Var4)) and
	   ((Quest.Var7)==0 or Player.CheckBuff(Quest.Var7)) then
    return 1
	else
		return 0
	end 

   return 1;
end

function Report_Run()
   
    Player.RemoveItem(Quest.Var3,Quest.Var4)
    Player.AddItem(Quest.Var5,Quest.Var6)
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
	Player.RemoveItem(Quest.Var3,Quest.Var4)
    Player.RemoveItem(Quest.Var5,Quest.Var6)
    Quest.SetQuestFlag(Quest.Var2,0)
    Player.MobAppear(Quest.Var13, true)
    Player.MobAppear(Quest.Var14, false)
    Player.MobAppear(Quest.Var17, true)
    Player.MobAppear(Quest.Var18, false)
    return 1;
end
