--# Var1 = 所要檢查機關的ID-1
--# Var2 = 所要檢查機關的狀態
--# Var3 = 所要檢查機關的ID-2
--# Var4 = 所要檢查機關的狀態
--# Var9 = 2014-4-17開發版未使用-使用前需再check

function ScriptStart()
  local S1 = Trigger.GetTriggerStatus(Trigger.Var1);
  local S2 = Trigger.GetTriggerStatus(Trigger.Var3);
  if((S1 ~= Trigger.Var2)or(S2 ~= Trigger.Var4))then
    return 0
  else
  Instance.CallScoreCount();
  Trigger.NextStatus();
    return 1
  end
end