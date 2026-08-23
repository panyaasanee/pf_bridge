--# Var1 = 所要關閉的配置區ID

function ScriptStart()

  Scene.PlacementOFF(Trigger.Var1);
  Trigger.NextStatus();
  return 1

end