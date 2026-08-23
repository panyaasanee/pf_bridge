--# Var1 = 所要檢查的道具
--# Var2 = 所要檢查的道具數量
--# Var3 = 所要檢查的BUFF ID

function ScriptStart()

  local I = Player.GetItemNum(Trigger.Var1);
  local B = Player.CheckBuff(Trigger.Var3) 

  if (I < Trigger.Var2)or(B == false) then
    return 0

  else
  Player.RemoveItem(Trigger.Var1,Trigger.Var2);
  Trigger.NextStatus();
    return 1
  end
end