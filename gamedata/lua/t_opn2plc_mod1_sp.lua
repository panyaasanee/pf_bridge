--# Var1 = 所要開啟的場景配置區ID-1
--# Var2 = 要檢查生或死怪物的配置區ID
--# Var3 = 所要開啟的場景配置區ID-2

function ScriptStart()
  local M = Scene.CheckPlacementAlive(Trigger.Var2);

  if(M == true)then
  Trigger.NextStatus();
    return 1

  else
  Scene.PlacementON(Trigger.Var1);
  Scene.PlacementON(Trigger.Var3);
  Trigger.NextStatus();
    return 1
  end
end