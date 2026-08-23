--# Var1 = 要檢查生或死怪物的配置區ID
--# Var9 = 2014-4-17開發版未使用-使用前需再check

function ScriptStart()

  local M = Scene.CheckPlacementAlive(Trigger.Var1);
  if(M == true)then
    return 0
  
  else
  Trigger.HideModel();
  Trigger.NextStatus();
    return 1
  end
end