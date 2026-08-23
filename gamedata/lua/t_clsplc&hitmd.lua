--# Var1 = 所要關閉的配置區ID
--# Var2 = 所要隱藏的Trigger
function ScriptStart()

  Scene.PlacementOFF(Trigger.Var1);
  Trigger.HideTriggerModel();
  Trigger.NextStatus();
  return 1

end