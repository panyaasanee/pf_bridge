--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 需要並扣除道具的ID
--# Var3 = 需要並扣除道具的數量
--# Var4 = 所要回收的場景配置區ID
--# Var5 = 沒事情發生時的回饋訊息
--# Var6 = 發生事件時的回饋訊息

function ScriptStart()

  local I = Player.GetItemNum(Trigger.Var2);
  if(I < Trigger.Var3)then
  Player.ShowMessage(Trigger.Var5)
    return 0

  else
  Player.RemoveItem(Trigger.Var2,Trigger.Var3);
  Scene.PlacementON(Trigger.Var1);
  Scene.PlacementCancel(Trigger.Var4);
  Player.ShowMessage(Trigger.Var6)
  Trigger.NextStatus();
    return 1
  end
end