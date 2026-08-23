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

function ScriptStart()
  local S1 = Trigger.GetTriggerStatus(Trigger.Var1);
  local S2 = Trigger.GetTriggerStatus(Trigger.Var2);
  if((S1 ~= Trigger.Var3) and (S2 ~= Trigger.Var4))then
    return 0
  
  else
  Trigger.StartTriggerAnimation(Trigger.Var1,Trigger.Var5,Trigger.Var6,1); 
  Trigger.StartTriggerAnimation(Trigger.Var2,Trigger.Var7,Trigger.Var8,1); 
  Trigger.SetTriggerStatus(Trigger.Var1,Trigger.Var9);
  Trigger.SetTriggerStatus(Trigger.Var2,Trigger.Var10);
  Trigger.NextStatus()
    return 1
  end;
end