--# Var1 = 機關所要施放的技能
--# Var2 = 所要檢查道具的ID(鑰匙)
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var2);
  if(I == 0)then
    return 0

  else  
  Trigger.CastSkillBy(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end