--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 需要並扣除道具的ID
--# Var3 = 需要並扣除道具的數量
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local I = Player.GetItemNum(Trigger.Var2);
  if(I < Trigger.Var3)then
    return 0

  else
  Player.RemoveItem(Trigger.Var2,Trigger.Var3);
  Scene.PlacementON(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end