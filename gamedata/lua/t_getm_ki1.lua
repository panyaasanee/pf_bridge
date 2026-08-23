--# Var1 = 給予玩家道具的ID
--# Var2 = 道具最多持有數量
--# Var3 = 檢查是否有此道具
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local I1 = Player.GetItemNum(Trigger.Var1);
  local I2 = Player.GetItemNum(Trigger.Var3);

  if(I1 >= Trigger.Var2)then
    return 0
  elseif(I2 == 0)then
    return 0

  else
  Player.AddItem(Trigger.Var1,1)
  Trigger.NextStatus();
    return 1
  end
end