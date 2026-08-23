--# Var1 = 所要關閉的配置區ID-1
--# Var2 = 所要關閉的配置區ID-2
--# Var3 = 所要關閉的配置區ID-3
--# Var4 = 所要關閉的配置區ID-4
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Scene.PlacementCancel(Trigger.Var1);
  Scene.PlacementCancel(Trigger.Var2);  
  Scene.PlacementCancel(Trigger.Var3);
  Scene.PlacementCancel(Trigger.Var4);
  Trigger.NextStatus();
  return 1
end