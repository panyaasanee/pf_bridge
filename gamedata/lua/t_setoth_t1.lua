--# Var1 = 所要控制機關的ID
--# Var2 = 所要控制機關的初始狀態
--# Var3 = 所要控制機關的指定狀態
--# Var4 = 所要檢查機關的ID
--# Var5 = 所要檢查機關的狀態
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local S1 = Trigger.GetTriggerStatus(Trigger.Var1);
  local S2 = Trigger.GetTriggerStatus(Trigger.Var4);
  if(S1 ~= Trigger.Var2)then
    return 0
  elseif(S2 ~= Trigger.Var5)then
    return 0

  else
  Trigger.SetTriggerStatus(Trigger.Var1,Trigger.Var3);
  Trigger.NextStatus();
    return 1
  end
end