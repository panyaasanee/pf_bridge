--# Var1 = 機關所要施放的技能
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  
  Trigger.CastSkillBy(Trigger.Var1);
  Trigger.NextStatus();
  return 1
end