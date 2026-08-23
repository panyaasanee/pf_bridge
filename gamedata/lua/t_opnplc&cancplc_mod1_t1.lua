--# Var1 = 所要檢查機關的ID
--# Var2 = 所要檢查機關的狀態
--# Var3 = 所要關閉並回收的配置區ID
--# Var4 = 所要開啟的場景配置區ID
--# Var5 = 所要檢查怪物的配置區ID
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local S = Trigger.GetTriggerStatus(Trigger.Var1);
  local M = Scene.CheckPlacementAlive(Trigger.Var5);
  if(S ~= Trigger.Var2)or(M == false)then
    return 0

  else
  Scene.PlacementCancel(Trigger.Var3);
  Scene.PlacementON(Trigger.Var4);
  Trigger.NextStatus();
    return 1
  end
end