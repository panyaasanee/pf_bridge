--# Var1 = 所要開啟的場景配置區ID-1
--# Var2 = 所要開啟的場景配置區ID-2
--# Var3 = 所要開啟的場景配置區ID-3
--# Var4 = 所要開啟的場景配置區ID-4
--# Var5 = 所要開啟的場景配置區ID-5
--# Var6 = 所要開啟的場景配置區ID-6

function ScriptStart()

  Scene.PlacementON(Trigger.Var1);
  Scene.PlacementON(Trigger.Var2);
  Scene.PlacementON(Trigger.Var3);
  Scene.PlacementON(Trigger.Var4);
  Scene.PlacementON(Trigger.Var5);
  Scene.PlacementON(Trigger.Var6);
  Trigger.NextStatus();
  return 1

end