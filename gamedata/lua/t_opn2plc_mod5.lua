--# Var1 = 所要開啟的場景配置區ID-1
--# Var2 = 所要開啟的場景配置區ID-2
--# Var3 = 要檢查生或死怪物的配置區ID-1
--# Var4 = 要檢查生或死怪物的配置區ID-2
--# Var5 = 要檢查生或死怪物的配置區ID-3
--# Var6 = 要檢查生或死怪物的配置區ID-4
--# Var7 = 要檢查生或死怪物的配置區ID-5

function ScriptStart()
  local M1 = Scene.CheckPlacementAlive(Trigger.Var3);
  local M2 = Scene.CheckPlacementAlive(Trigger.Var4);
  local M3 = Scene.CheckPlacementAlive(Trigger.Var5);
  local M4 = Scene.CheckPlacementAlive(Trigger.Var6);
  local M5 = Scene.CheckPlacementAlive(Trigger.Var7);

  if((M1 == true)or(M2 == true)or(M3 == true)or(M4 == true)or(M5 == true))then
    return 0

  else
  Scene.PlacementON(Trigger.Var1);
  Scene.PlacementON(Trigger.Var2); 
  Trigger.NextStatus();
    return 1
  end
end