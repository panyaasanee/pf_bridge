--# Var1 = 前置機關ID
--# Var2 = 前置機關要符合的狀態

function ScriptStart()

  if (Trigger.GetTriggerStatus(Trigger.Var1) ~= Trigger.Var2) then
    return 0 
  else
  Trigger.NextStatus();
    return 1
  end
end