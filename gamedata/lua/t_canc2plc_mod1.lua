--# Var1 = 所要關閉的配置區ID-1
--# Var2 = 所要關閉的配置區ID-2
--# Var3 = 所要檢查怪物的配置區ID

function ScriptStart()
  local M = Scene.CheckPlacementAlive(Trigger.Var3);
  if(M == true)then
    return 0

  else
  Scene.PlacementCancel(Trigger.Var1);
  Scene.PlacementCancel(Trigger.Var2);
  Trigger.NextStatus();
    return 1
  end
end