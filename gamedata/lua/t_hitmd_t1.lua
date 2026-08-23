--# Var1 = 所要檢查機關的ID
--# Var2 = 所要檢查機關的狀態

function ScriptStart()
	if(Trigger.GetTriggerStatus(Trigger.Var1) == Trigger.Var2)then
		Trigger.HideTriggerModel(Trigger.Var1);
		Trigger.NextStatus();
		return 1	
	else
		return 0
	end
end