--# Var1 = 給予玩家道具的ID
--# Var2 = 道具最多持有數量
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var1);
  if(I >= Trigger.Var2)then
    return 0

  else
  Player.AddItem(Trigger.Var1,1)
  Trigger.NextStatus();
    return 1
  end
end