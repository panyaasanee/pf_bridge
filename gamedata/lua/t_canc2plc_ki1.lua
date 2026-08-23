--# Var1 = 所要關閉的配置區ID-1
--# Var2 = 所要關閉的配置區ID-2
--# Var3 = 身上要有的道具ID

function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var3);
  if(I == 0)then
    return 0
  else
  Scene.PlacementCancel(Trigger.Var1);
  Scene.PlacementCancel(Trigger.Var2);
  Trigger.NextStatus();
    return 1
  end
end