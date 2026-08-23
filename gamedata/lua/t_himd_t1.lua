--# Var1 = 所要檢查機關的ID
--# Var2 = 所要檢查機關的狀態

function ScriptStart()
  local S = Trigger.GetTriggerStatus(Trigger.Var1);
  if(S ~= Trigger.Var2)then
    return 0

  else
  Trigger.HideModel();
  Trigger.NextStatus();
    return 1
  end
end