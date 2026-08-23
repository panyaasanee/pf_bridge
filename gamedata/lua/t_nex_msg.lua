--# Var1 = 訊息類型(1個人2隊伍3場景4分流)
--# Var2 = 系統訊息編號

function ScriptStart()

	if (Trigger.Var1 == 1)then
		Trigger.TriggerShowMessage(0,Trigger.Var2)
		Trigger.NextStatus();
		return 1	
		
	elseif (Trigger.Var1 == 2)then
		Trigger.TriggerShowMessage(1,Trigger.Var2)
		Trigger.NextStatus();
		return 1	
		
	elseif (Trigger.Var1 == 3)then
		Trigger.TriggerShowMessage(2,Trigger.Var2)
		Trigger.NextStatus();
		return 1	
		
	elseif (Trigger.Var1 == 4)then
		Trigger.TriggerShowMessage(3,Trigger.Var2)
		Trigger.NextStatus();
		return 1	
	else
		return 0
	end
end