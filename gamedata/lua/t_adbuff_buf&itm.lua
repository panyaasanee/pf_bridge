--# Var1 = 所要檢查的道具
--# Var2 = 所要檢查的道具數量
--# Var3 = 身上不能有，啟動後被強制施加的BuffID
--# Var4 = Buff的標準等級

function ScriptStart()

  local I = Player.GetItemNum(Trigger.Var1);
  local B = Player.CheckBuff(Trigger.Var3) 

  if (I < Trigger.Var2)then
    Player.ShowMessage(859)
    return 0
  elseif(B == true) then
    return 0
  else
  Player.RemoveItem(Trigger.Var1,Trigger.Var2);
  Player.AddBuff(Trigger.Var3,Trigger.Var4);
  Trigger.NextStatus();
    return 1
  end
end