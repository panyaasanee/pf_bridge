--# Var1 = 所要控制機關的ID
--# Var2 = 所要控制機關的初始狀態
--# Var3 = 所要控制機關的指定狀態

function ScriptStart()

  local S = Trigger.GetTriggerStatus(Trigger.Var1);
  if(S ~= Trigger.Var2)then
    return 0

  else
  Trigger.SetTriggerStatus(Trigger.Var1,Trigger.Var3);
  Trigger.NextStatus();
    return 1
  end
end