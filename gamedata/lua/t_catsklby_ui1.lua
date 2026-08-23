--# Var1 = 機關所要施放的技能
--# Var2 = 所要檢查並扣除道具的ID
--# Var2 = 所要撿柴並扣除道具的數量
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var2);
  if(I < Trigger.Var3)then
    return 0

  else
  Trigger.CastSkillBy(Trigger.Var1);
  Player.RemoveItem(Trigger.Var2,Trigger.Var3);
  Trigger.NextStatus();
    return 1
  end
end