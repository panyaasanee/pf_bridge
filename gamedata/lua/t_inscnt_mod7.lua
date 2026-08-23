--# Var1 = 要檢查生或死怪物的配置區ID-1
--# Var2 = 要檢查生或死怪物的配置區ID-2
--# Var3 = 要檢查生或死怪物的配置區ID-3
--# Var4 = 要檢查生或死怪物的配置區ID-4
--# Var5 = 要檢查生或死怪物的配置區ID-5
--# Var6 = 要檢查生或死怪物的配置區ID-6
--# Var7 = 要檢查生或死怪物的配置區ID-7
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local M1 = Scene.CheckPlacementAlive(Trigger.Var1);
  local M2 = Scene.CheckPlacementAlive(Trigger.Var2);
  local M3 = Scene.CheckPlacementAlive(Trigger.Var3);
  local M4 = Scene.CheckPlacementAlive(Trigger.Var4);
  local M5 = Scene.CheckPlacementAlive(Trigger.Var5);
  local M6 = Scene.CheckPlacementAlive(Trigger.Var6);
  local M7 = Scene.CheckPlacementAlive(Trigger.Var7);

  if((M1 == true)or(M2 == true)or(M3 == true)or(M4 == true)or(M5 == true)or(M6 == true)or(M7 == true))then
    return 0
  else
  Instance.CallScoreCount();
  Trigger.NextStatus();
    return 1
  end
end