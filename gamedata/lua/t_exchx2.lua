--# Var1 = 扣除的道具ID
--# Var2 = 扣除的道具數量
--# Var3 = 兌換獲得的道具ID
--# Var4 = 兌換獲得的道具數量
--# Var5 = 扣除的道具2ID
--# Var6 = 扣除的道具2數量
function ScriptStart()

  if(Player.GetItemNum(Trigger.Var1) < Trigger.Var2) or (Player.GetItemNum(Trigger.Var5) < Trigger.Var6)then
    return 0

  else
  Player.RemoveItem(Trigger.Var1,Trigger.Var2);
  Player.RemoveItem(Trigger.Var5,Trigger.Var6);  
  Player.AddItem(Trigger.Var3,Trigger.Var4);
  Trigger.NextStatus();
    return 1
  end
end