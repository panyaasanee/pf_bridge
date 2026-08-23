--# Var1 = 要對觸發者施放的技能-1
--# Var2 = 要對觸發者施放的技能-2
--# Var3 = 要對觸發者施放的技能-3
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Player.CastSkillAt(Trigger.Var1);
  Player.CastSkillAt(Trigger.Var2);
  Player.CastSkillAt(Trigger.Var3);
  Trigger.NextStatus();
  return 1

end