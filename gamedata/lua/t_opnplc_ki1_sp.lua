--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 需求道具的ID(鑰匙)
--# Var3 = 需求道具的數量

function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var2)
  if(I ~= Trigger.Var3)then
	return 0

  else
  Scene.PlacementON(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end