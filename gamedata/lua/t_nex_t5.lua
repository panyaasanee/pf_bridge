--# Var1 = 前置機關ID-1
--# Var2 = 前置機關ID-2
--# Var3 = 前置機關ID-3
--# Var4 = 前置機關ID-4
--# Var5 = 前置機關ID-5
--# Var6 = 以上5個機關都要為此狀態

function ScriptStart()

  local S1 = Trigger.GetTriggerStatus(Trigger.Var1);
  local S2 = Trigger.GetTriggerStatus(Trigger.Var2);
  local S3 = Trigger.GetTriggerStatus(Trigger.Var3);
  local S4 = Trigger.GetTriggerStatus(Trigger.Var4);
  local S5 = Trigger.GetTriggerStatus(Trigger.Var5);

  if ((S1 ~= Trigger.Var6)or(S2 ~= Trigger.Var6)or(S3 ~= Trigger.Var6)or(S4 ~= Trigger.Var6)or(S5 ~= Trigger.Var6)) then
    return 0 
  else
  Trigger.NextStatus();
    return 1
  end
end