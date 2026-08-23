--# Var1 = 所要控制機關的ID
--# Var2 = 所要控制機關的初始狀態
--# Var3 = 所要控制機關的指定狀態
--# Var4 = 要檢查生或死的怪物ID
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local S = Trigger.GetTriggerStatus(Trigger.Var1);
  local M = Mob.CheckMobalive(Trigger.Var4);
  if(S ~= Trigger.Var2)then
    return 0
  elseif(M ~= true)then
    return 0

  else
  Trigger.SetTriggerStatus(Trigger.Var1,Trigger.Var3);
  Trigger.NextStatus();
    return 1
  end
end