--# Var1 = 所要開啟的場景配置區ID

function ScriptStart()

  Scene.PlacementON(Trigger.Var1);
  Trigger.NextStatus();
  return 1

end