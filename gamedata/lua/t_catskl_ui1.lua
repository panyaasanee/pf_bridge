--# Var1 = 玩家藉由機關所要施放的技能
--# Var2 = 所要檢查並扣除道具的ID
--# Var3 = 所要撿查並扣除道具的數量

function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var2);
  if(I < Trigger.Var3)then
    Player.ShowMessage(859)
    return 0

  else
  Trigger.CastSkill(Trigger.Var1);
  Player.RemoveItem(Trigger.Var2,Trigger.Var3);
  Trigger.NextStatus();
    return 1
  end
end