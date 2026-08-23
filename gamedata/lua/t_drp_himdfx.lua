--# Var1 = 所要執行的掉落群

function ScriptStart()

  Player.DropProcess(Trigger.Var1);
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");  
  Trigger.NextStatus();
  return 1

end