--# Var1 = 動態起始Frame
--# Var2 = 動態結束Frame
--# Var3 = 要檢查生或死怪物的配置區ID

function ScriptStart()
  local M = Scene.CheckPlacementAlive(Trigger.Var3);
  
  if(M == true)then
    return 0  
  else
  Trigger.StartAnimation(Trigger.Var1,Trigger.Var2,1); 
  Trigger.NextStatus();
    return 1
  end;
end