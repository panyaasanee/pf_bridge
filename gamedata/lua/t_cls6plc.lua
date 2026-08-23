--# Var1 = 所要關閉的配置區ID-1
--# Var2 = 所要關閉的配置區ID-2
--# Var3 = 所要關閉的配置區ID-3
--# Var4 = 所要關閉的配置區ID-4
--# Var5 = 所要關閉的配置區ID-5
--# Var6 = 所要關閉的配置區ID-6
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Scene.PlacementOFF(Trigger.Var1);
  Scene.PlacementOFF(Trigger.Var2);
  Scene.PlacementOFF(Trigger.Var3);
  Scene.PlacementOFF(Trigger.Var4);
  Scene.PlacementOFF(Trigger.Var5);
  Scene.PlacementOFF(Trigger.Var6);
  Trigger.NextStatus();
  return 1

end