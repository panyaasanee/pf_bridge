--# Var1 = 所要檢查機關的ID
--# Var2 = 所要檢查機關的狀態
--# Var3 = 所要開啟的場景配置區ID-1
--# Var4 = 所要開啟的場景配置區ID-2
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local S = Trigger.GetTriggerStatus(Trigger.Var1);
  if(S ~= Trigger.Var2)then
    return 0

  else
  Scene.PlacementON(Trigger.Var3);
  Scene.PlacementON(Trigger.Var4);
  Trigger.NextStatus();
   return 1
  end
end