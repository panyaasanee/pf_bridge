--# Var1 = 所要關閉的配置區ID-1
--# Var2 = 所要關閉的配置區ID-2
function ScriptStart()

  Scene.PlacementOFF(Trigger.Var1);
  Scene.PlacementOFF(Trigger.Var2);  
  Trigger.NextStatus();
  return 1

end