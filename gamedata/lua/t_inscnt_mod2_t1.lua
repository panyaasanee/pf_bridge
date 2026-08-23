--# Var1 = 要檢查生或死怪物的配置區ID-1
--# Var2 = 要檢查生或死怪物的配置區ID-2
--# Var3 = 要檢查之機關的ID
--# Var4 = 要檢查之機關的狀態值

function ScriptStart()
  local M1 = Scene.CheckPlacementAlive(Trigger.Var1);
  local M2 = Scene.CheckPlacementAlive(Trigger.Var2); 
  local S = Trigger.GetTriggerStatus(Trigger.Var3);
  if((M1 == true)or(M2 == true)or(S ~= Trigger.Var4))then
    return 0

  else
  Instance.CallScoreCount();
  Trigger.NextStatus();
    return 1
  end
end