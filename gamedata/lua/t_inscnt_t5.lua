--# Var1 = 所要檢查機關的ID-1
--# Var2 = 所要檢查機關1的狀態
--# Var3 = 所要檢查機關的ID-2
--# Var4 = 所要檢查機關2的狀態
--# Var5 = 所要檢查機關的ID-3
--# Var6 = 所要檢查機關3的狀態
--# Var7 = 所要檢查機關的ID-4
--# Var8 = 所要檢查機關4的狀態
--# Var9 = 所要檢查機關的ID-5
--# Var10 = 所要檢查機關5的狀態
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local S1 = Trigger.GetTriggerStatus(Trigger.Var1);
  local S2 = Trigger.GetTriggerStatus(Trigger.Var3);
  local S3 = Trigger.GetTriggerStatus(Trigger.Var5);
  local S4 = Trigger.GetTriggerStatus(Trigger.Var7);
  local S5 = Trigger.GetTriggerStatus(Trigger.Var9);
  if((S1 ~= Trigger.Var2)or(S2 ~= Trigger.Var4)or(S3 ~= Trigger.Var6)or(S4 ~= Trigger.Var8)or(S5 ~= Trigger.Var10))then
    return 0
  else
  Instance.CallScoreCount();
  Trigger.NextStatus();
    return 1
  end
end