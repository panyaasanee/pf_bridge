--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 所要檢查機關的ID-1
--# Var3 = 所要檢查機關的狀態-1
--# Var4 = 所要檢查機關的ID-2
--# Var5 = 所要檢查機關的狀態-2

function ScriptStart()
  local S1 = Trigger.GetTriggerStatus(Trigger.Var2);
  local S2 = Trigger.GetTriggerStatus(Trigger.Var4);
  if((S1 ~= Trigger.Var3)and(S2 ~= Trigger.Var5))then
    return 0

  else
  Scene.PlacementON(Trigger.Var1);
  Trigger.NextStatus();
   return 1
  end
end