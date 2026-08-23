--# Var1 = 前置機關ID-1
--# Var2 = 前置機關要符合的狀態-1
--# Var3 = 前置機關ID-2
--# Var4 = 前置機關要符合的狀態-2

function ScriptStart()

  if (Trigger.GetTriggerStatus(Trigger.Var1) ~= Trigger.Var2)and(Trigger.GetTriggerStatus(Trigger.Var3) ~= Trigger.Var4)then
    return 0 
  else
  Trigger.NextStatus();
    return 1
  end
end