--# Var1 = 要對觸發者施放的技能
--# Var2 = 所需要的道具ID(鑰匙)
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var2);
  if(I == 0)then
    return 0
  else
  Player.CastSkillAt(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end