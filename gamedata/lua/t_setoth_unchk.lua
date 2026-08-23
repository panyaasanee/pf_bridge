--# Var1 = 所要控制機關的ID
--# Var2 = 所要控制機關的指定狀態

function ScriptStart()

  Trigger.SetTriggerStatus(Trigger.Var1,Trigger.Var2);
  Trigger.NextStatus();
    return 1
end