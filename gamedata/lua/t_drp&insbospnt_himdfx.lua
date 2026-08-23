--# Var1 = 所要執行的掉落群
--# Var2 = 需要扣除的道具ID

function ScriptStart()

  local I = Player.GetItemNum(Trigger.Var2)
  
  if I == 0 then
    Player.ShowMessage(859)
    return 0
	
  else
  Player.DropProcess(Trigger.Var1);
  Player.RemoveItem(Trigger.Var2,1)
  Instance.AddBonusPoint()
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");  
  Trigger.NextStatus();
    return 1
  end
end