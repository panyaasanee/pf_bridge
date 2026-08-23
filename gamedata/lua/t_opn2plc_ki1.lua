--# Var1 = 需求道具的ID(鑰匙)
--# Var2 = 所要開啟的場景配置區ID-1
--# Var3 = 所要開啟的場景配置區ID-2

function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var1)
  if(I == 0)then 
    return 0

  else
  Scene.PlacementON(Trigger.Var2);
  Scene.PlacementON(Trigger.Var3);
  Trigger.NextStatus();
    return 1
  end
end