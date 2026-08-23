--# Var1 = 所要關閉的配置區ID
--# Var2 = 所要檢查機關的ID
--# Var3 = 所要檢查機關的狀態


function ScriptStart()
	if(Trigger.GetTriggerStatus(Trigger.Var2) ~= Trigger.Var3)then
		return 0
	else
		Scene.PlacementCancel(Trigger.Var1);
		Trigger.NextStatus();
		return 1
	end	
end