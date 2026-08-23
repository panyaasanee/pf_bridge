--# Var1 = 要檢查生或死怪物的配置區ID-1
--# Var2 = 要檢查之機關的ID
--# Var3 = 要檢查之機關的狀態值

function ScriptStart()
  local M = Scene.CheckPlacementAlive(Trigger.Var1);
  local S = Trigger.GetTriggerStatus(Trigger.Var2);
  if((M == true)or(S ~= Trigger.Var3))then
    return 0

  else
  Instance.CallScoreCount();
  Trigger.NextStatus();
    return 1
  end
end