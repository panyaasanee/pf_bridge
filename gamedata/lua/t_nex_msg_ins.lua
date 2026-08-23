--# Var1 = 訊息類型(1個人2隊伍3場景4分流)
--# Var2 = 系統訊息編號
--# Var3 = 副本(0=不需指定副本;1=一個副本;2=兩個副本)
--# Var4 = 副本編號1
--# Var5 = 副本編號2

function ScriptStart()
	if (Trigger.Var3 == 0)then
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
	elseif (Trigger.Var3 == 1)then
		if (Instance.GetInstanceID() == Trigger.Var4)then
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
		else
			return 0
		end
	elseif (Trigger.Var3 == 2)then
		if (Instance.GetInstanceID() == Trigger.Var4) or (Instance.GetInstanceID() == Trigger.Var5)then
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
		else
			return 0
		end	
	else
		return 0
	end
	
end