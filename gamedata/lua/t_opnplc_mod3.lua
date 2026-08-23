--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 要檢查生或死怪物的配置區ID-1
--# Var3 = 要檢查生或死怪物的配置區ID-2
--# Var4 = 要檢查生或死怪物的配置區ID-3

function ScriptStart()
  local M1 = Scene.CheckPlacementAlive(Trigger.Var2);
  local M2 = Scene.CheckPlacementAlive(Trigger.Var3);
  local M3 = Scene.CheckPlacementAlive(Trigger.Var4);

  if((M1 == true)or(M2 == true)or(M3 == true))then
    return 0

  else
  Scene.PlacementON(Trigger.Var1);
  Trigger.NextStatus();
  return 1
  end

end