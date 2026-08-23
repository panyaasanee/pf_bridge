--# Var1 = 要受控制機關1的ID
--# Var2 = 要受控制機關2的ID
--# Var3 = 受控制機關1的初始狀態
--# Var4 = 受控制機關2的初始狀態
--# Var5 = 機關1動態起始Frame
--# Var6 = 機關1動態結束Frame
--# Var7 = 機關2動態起始Frame
--# Var8 = 機關2動態結束Frame
--# Var9 = 受控制機關1的作用後狀態
--# Var10 = 受控制機關2的作用後狀態
--# Var11 = 訊息類型(1個人2隊伍3場景4分流)
--# Var12 = 開啟時播放的訊息

function ScriptStart()

	if((Trigger.GetTriggerStatus(Trigger.Var1) ~= Trigger.Var3) and (Trigger.GetTriggerStatus(Trigger.Var2) ~= Trigger.Var4))then
		return 0
	else
		if (Trigger.Var11 == 1)then
			Trigger.TriggerShowMessage(0,Trigger.Var12)
			Trigger.StartTriggerAnimation(Trigger.Var1,Trigger.Var5,Trigger.Var6,1); 
			Trigger.StartTriggerAnimation(Trigger.Var2,Trigger.Var7,Trigger.Var8,1); 
			Trigger.SetTriggerStatus(Trigger.Var1,Trigger.Var9);
			Trigger.SetTriggerStatus(Trigger.Var2,Trigger.Var10);
			Trigger.NextStatus();
			return 1	
		
		elseif (Trigger.Var11 == 2)then
			Trigger.TriggerShowMessage(1,Trigger.Var12)
			Trigger.StartTriggerAnimation(Trigger.Var1,Trigger.Var5,Trigger.Var6,1); 
			Trigger.StartTriggerAnimation(Trigger.Var2,Trigger.Var7,Trigger.Var8,1); 
			Trigger.SetTriggerStatus(Trigger.Var1,Trigger.Var9);
			Trigger.SetTriggerStatus(Trigger.Var2,Trigger.Var10);
			Trigger.NextStatus();
			return 1	
		
		elseif (Trigger.Var11 == 3)then
			Trigger.TriggerShowMessage(2,Trigger.Var12)
			Trigger.StartTriggerAnimation(Trigger.Var1,Trigger.Var5,Trigger.Var6,1); 
			Trigger.StartTriggerAnimation(Trigger.Var2,Trigger.Var7,Trigger.Var8,1); 
			Trigger.SetTriggerStatus(Trigger.Var1,Trigger.Var9);
			Trigger.SetTriggerStatus(Trigger.Var2,Trigger.Var10);
			Trigger.NextStatus();
			return 1	
		
		elseif (Trigger.Var11 == 4)then
			Trigger.TriggerShowMessage(3,Trigger.Var12)
			Trigger.StartTriggerAnimation(Trigger.Var1,Trigger.Var5,Trigger.Var6,1); 
			Trigger.StartTriggerAnimation(Trigger.Var2,Trigger.Var7,Trigger.Var8,1); 
			Trigger.SetTriggerStatus(Trigger.Var1,Trigger.Var9);
			Trigger.SetTriggerStatus(Trigger.Var2,Trigger.Var10);
			Trigger.NextStatus();
			return 1	
		else
			return 0
		end
		
		return 0
	end
end