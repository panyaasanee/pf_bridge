--# Var1 = 要檢查生或死怪物的配置區ID
--# Var2 = 觸發機關所扣除的關鍵事件次數

function ScriptStart()

  local M = Scene.CheckPlacementAlive(Trigger.Var1);
  if(M == true)then
    return 0

  else
  Instance.RemoveKeyEvent(Trigger.Var2);
  Trigger.NextStatus();
    return 1
  end
end