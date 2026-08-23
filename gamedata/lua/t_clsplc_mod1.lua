--# Var1 = 所要關閉的配置區ID
--# Var2 = 所要檢查怪物的配置區ID

function ScriptStart()
  local M = Scene.CheckPlacementAlive(Trigger.Var2);
  if(M == true)then
    return 0

  else
  Scene.PlacementOFF(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end