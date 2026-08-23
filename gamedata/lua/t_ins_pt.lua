--# Var1 = 所要產生的副本群組
--# Var2 = 等級限制

function ScriptStart()

local LV = Player.GetLv()

	if (LV < Trigger.Var2) then 
		Player.ShowMessage(4)	
		return 0
	else
		Player.LoadInstanceGroup(Trigger.Var1);
		return 1
	end

end
