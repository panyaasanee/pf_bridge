--# Var1 = 要對觸發者施放的技能
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Player.CastSkillAt(Trigger.Var1);
  Trigger.NextStatus();
  return 1

end