--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 訊息類型(1個人2隊伍3場景4分流)
--# Var3 = 系統訊息編號
function ScriptStart()
	if (Trigger.Var2 == 1)then
		Trigger.TriggerShowMessage(0,Trigger.Var3)
		Scene.PlacementON(Trigger.Var1);
		Trigger.NextStatus();
		return 1	
		
	elseif (Trigger.Var2 == 2)then
		Trigger.TriggerShowMessage(1,Trigger.Var3)
		Scene.PlacementON(Trigger.Var1);
		Trigger.NextStatus();
		return 1	
		
	elseif (Trigger.Var2 == 3)then
		Trigger.TriggerShowMessage(2,Trigger.Var3)
		Scene.PlacementON(Trigger.Var1);
		Trigger.NextStatus();
		return 1	
		
	elseif (Trigger.Var2 == 4)then
		Trigger.TriggerShowMessage(3,Trigger.Var3)
		Scene.PlacementON(Trigger.Var1);
		Trigger.NextStatus();
		return 1	
	else
		return 0
	end
end