--# Var1 = 所要執行的掉落群
--# Var2 = 要扣除道具的ID
--# Var3 = 要扣除道具的數量

function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var2);
  
  if(I < Trigger.Var3)then
    Player.ShowMessage(859)
    return 0  

  else
  Player.DropProcess(Trigger.Var1);
  Player.RemoveItem(Trigger.Var2,Trigger.Var3); 
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");  
  Trigger.NextStatus();
    return 1
  end
end