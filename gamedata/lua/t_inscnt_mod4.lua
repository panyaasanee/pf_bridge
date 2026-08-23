--# Var1 = 要檢查生或死怪物的配置區ID-1
--# Var2 = 要檢查生或死怪物的配置區ID-2
--# Var3 = 要檢查生或死怪物的配置區ID-3
--# Var4 = 要檢查生或死怪物的配置區ID-4

function ScriptStart()
  local M1 = Scene.CheckPlacementAlive(Trigger.Var1);
  local M2 = Scene.CheckPlacementAlive(Trigger.Var2);
  local M3 = Scene.CheckPlacementAlive(Trigger.Var3);
  local M4 = Scene.CheckPlacementAlive(Trigger.Var4);
  if((M1 == true)or(M2 == true)or(M3 == true)or(M4 == true))then
    return 0
  else
  Instance.CallScoreCount();
  Trigger.NextStatus();
    return 1
  end
end