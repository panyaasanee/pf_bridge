--# Var1 = 要對觸發者施放的技能

function ScriptStart()

  Player.CastSkillAt(Trigger.Var1);
  Trigger.HideModel();
  Trigger.NextStatus();
  return 1
end