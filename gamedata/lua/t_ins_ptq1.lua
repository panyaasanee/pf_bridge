--# Var1 = 所要產生的副本群組
--# Var2 = 所要檢查的任務
--# Var3 = 所檢查任務要符合的旗標值

function ScriptStart()

	if(Quest.GetQuestFlag(Trigger.Var2) ~= Trigger.Var3) then
		Player.ShowMessage(4)	
		return 0
	else
		Player.LoadInstanceGroup(Trigger.Var1);
		return 1
	end

end
