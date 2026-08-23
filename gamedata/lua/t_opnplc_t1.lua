--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 所要檢查機關的ID
--# Var3 = 所要檢查機關的狀態

function ScriptStart()
  local S = Trigger.GetTriggerStatus(Trigger.Var2);
  if(S ~= Trigger.Var3)then
    return 0

  else
  Scene.PlacementON(Trigger.Var1);
  Trigger.NextStatus();
   return 1
  end
end