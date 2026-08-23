--# Var1 = 前置機關ID
--# Var2 = 前置機關要符合的狀態
--# Var3 = 副本(0=不需指定副本;1=一個副本;2=兩個副本)
--# Var4 = 副本編號1
--# Var5 = 副本編號2

function ScriptStart()

	if (Trigger.GetTriggerStatus(Trigger.Var1) == Trigger.Var2) then
		if (Trigger.Var3 == 0)then
			Trigger.NextStatus();
			return 1
			
		elseif (Trigger.Var3 == 1)then
			if (Instance.GetInstanceID() == Trigger.Var4)then
				Trigger.NextStatus();
				return 1
			end
			
		elseif  (Trigger.Var3 == 2)then
		if (Instance.GetInstanceID() == Trigger.Var4) or (Instance.GetInstanceID() == Trigger.Var5)then
				Trigger.NextStatus();
				return 1		
			end	
		else
			return 0
		end
	else
		return 0 
	end	
end