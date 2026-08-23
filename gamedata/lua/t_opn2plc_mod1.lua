--# Var1 = 所要開啟的場景配置區ID-1
--# Var2 = 要檢查生或死怪物的配置區ID
--# Var3 = 所要開啟的場景配置區ID-2
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local M = Scene.CheckPlacementAlive(Trigger.Var2);

  if(M == true)then
    return 0

  else
  Scene.PlacementON(Trigger.Var1);
  Scene.PlacementON(Trigger.Var3);
  Trigger.NextStatus();
    return 1
  end
end