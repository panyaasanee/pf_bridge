--# Var1 = 機關所要施放的技能
--# Var2 = 所要檢查機關的ID
--# Var3 = 所要檢查機關的狀態
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local S = Trigger.GetTriggerStatus(Trigger.Var2);
  if(S ~= Trigger.Var3)then
    return 0

  else
  Trigger.CastSkillBy(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end