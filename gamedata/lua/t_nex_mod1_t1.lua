--# Var1 = 要檢查生或死怪物的配置區ID
--# Var2 = 所要檢查的機關ID
--# Var3 = 所要檢查機關的狀態


function ScriptStart()

  local M = Scene.CheckPlacementAlive(Trigger.Var1);
  local S = Trigger.GetTriggerStatus(Trigger.Var2);

  if((M == true)or(S ~= Trigger.Var3))then
    return 0

  else
  Trigger.NextStatus();
    return 1
  end
end