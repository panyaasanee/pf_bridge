--# Var1 = 前置機關ID-1
--# Var2 = 前置機關-1要符合的狀態
--# Var3 = 前置機關ID-2
--# Var4 = 前置機關-2要符合的狀態
--# Var5 = 前置機關ID-3
--# Var6 = 前置機關-3要符合的狀態

function ScriptStart()

  local T1 = Trigger.GetTriggerStatus(Trigger.Var1);
  local T2 = Trigger.GetTriggerStatus(Trigger.Var3);
  local T3 = Trigger.GetTriggerStatus(Trigger.Var5);

  if ((T1 ~= Trigger.Var2)or(T2 ~= Trigger.Var4)or(T3 ~= Trigger.Var6)) then
    return 0 

  else
  Trigger.NextStatus();
    return 1
  end
end