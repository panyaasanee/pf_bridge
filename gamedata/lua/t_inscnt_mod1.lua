--# Var1 = 要檢查生或死怪物的配置區ID

function ScriptStart()
  local M = Scene.CheckPlacementAlive(Trigger.Var1);
  if(M == true)then
    return 0
  else
  Instance.CallScoreCount();
  Trigger.NextStatus();
    return 1
  end
end

