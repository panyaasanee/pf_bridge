--# Var1 = 神鬼鬥技場專用

function ScriptStart()

	if (Instance.GetInstanceID() == 1005)then --一星副本訊息廣播
		if (Trigger.GetTriggerStatus(13) == 2)then--大地撕裂者
			Trigger.TriggerShowMessage(2,914)
			return 1
		end
		if (Trigger.GetTriggerStatus(16) == 2)then--森魔使出場
			Trigger.TriggerShowMessage(2,915)
			return 1
		end
		if (Trigger.GetTriggerStatus(20) == 2)then--大地撕裂者var2
			Trigger.TriggerShowMessage(2,916)
			return 1
		end	
		if (Trigger.GetTriggerStatus(23) == 2)then--快結束了
			Trigger.TriggerShowMessage(2,917)
			return 1
		end	
		if (Trigger.GetTriggerStatus(26) == 2)then--BOSS登場
			Trigger.TriggerShowMessage(2,918)
			return 1
		end			
		if (Trigger.GetTriggerStatus(27) == 3)then--BOSS死亡
			Trigger.TriggerShowMessage(2,919)
			return 1
		end			
			
	elseif (Instance.GetInstanceID() == 1035)then --二星副本訊息廣播
		
		if (Trigger.GetTriggerStatus(13) == 2)then--火鳥
			Trigger.TriggerShowMessage(2,920)
			return 1
		end
		if (Trigger.GetTriggerStatus(20) == 2)then--菁英冒險者
			Trigger.TriggerShowMessage(2,921)
			return 1
		end	
		if (Trigger.GetTriggerStatus(23) == 2)then--快結束了
			Trigger.TriggerShowMessage(2,917)
			return 1
		end	
		if (Trigger.GetTriggerStatus(26) == 2)then--BOSS登場
			Trigger.TriggerShowMessage(2,918)
			return 1
		end			
		if (Trigger.GetTriggerStatus(27) == 3)then--BOSS死亡
			Trigger.TriggerShowMessage(2,919)
			return 1
		end	
		
	else
		return 0
	end
end