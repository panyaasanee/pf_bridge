--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 要檢查生或死怪物的配置區ID

function ScriptStart()
  local M = Scene.CheckPlacementAlive(Trigger.Var2);
  local T = Trigger.GetTriggerStatus(4);  

  if(M == true)or(T == 0)then
    return 0

  else
  Scene.PlacementON(Trigger.Var1);
  Trigger.NextStatus();
  return 1
  end

end