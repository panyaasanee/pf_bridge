--# Var1 = 要受控制機關1的ID
--# Var2 = 要受控制機關2的ID
--# Var3 = 要受控制機關3的ID
--# Var4 = 要受控制機關4的ID
--# Var5 = 要受控制機關5的ID
--# Var6 = 機關動態起始Frame
--# Var7 = 機關動態結束Frame
--# Var8 = 受控制機關的初始狀態
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local S1 = Trigger.GetTriggerStatus(Trigger.Var1);
  local S2 = Trigger.GetTriggerStatus(Trigger.Var2);
  local S3 = Trigger.GetTriggerStatus(Trigger.Var3);
  local S4 = Trigger.GetTriggerStatus(Trigger.Var4);
  local S5 = Trigger.GetTriggerStatus(Trigger.Var5);
  if((S1 ~= Trigger.Var8) and (S2 ~= Trigger.Var8) and(S3 ~= Trigger.Var8) and (S4 ~= Trigger.Var8) and (S5 ~= Trigger.Var8))then
    return 0
  
  else
  Trigger.StartTriggerAnimation(Trigger.Var1,Trigger.Var6,Trigger.Var7,1); 
  Trigger.StartTriggerAnimation(Trigger.Var2,Trigger.Var6,Trigger.Var7,1); 
  Trigger.StartTriggerAnimation(Trigger.Var3,Trigger.Var6,Trigger.Var7,1); 
  Trigger.StartTriggerAnimation(Trigger.Var4,Trigger.Var6,Trigger.Var7,1); 
  Trigger.StartTriggerAnimation(Trigger.Var5,Trigger.Var6,Trigger.Var7,1); 
  Trigger.NextStatus()
    return 1
  end;
end