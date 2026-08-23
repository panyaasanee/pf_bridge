function OpenAcceptUI_Run()
    Mob.ShowAnimation(Quest.StringVar1)
end 

function OpenReportUI_Run()
    Mob.ShowAnimation(Quest.StringVar2)
end 

function Accept_Check()

   return 1;
end

function Accept_Run()

	if Player.GetBoatHealth() ~= 100 then

		if Player.GetCash() >= Quest.Var2 then
		
			Player.BoatHealth(Quest.Var3)
			Player.AddCash(Quest.Var2 * -1)
			Player.ShowMessage(824) --船隻已修理
			
		else
		
			Player.ShowMessage(1) --金錢不足
			
		end
		Quest.SetFlag(Quest.None)
		
	else
	
		Player.ShowMessage(824) --生命值已滿
	
	end
	
    return 1
end


function Report_Check() 
        
    return 0
end

function Report_Run()
    
    return 1
end

function Delete_Run()
    
    return 1
end
