--# Var1 = 所要開啟的場景配置區ID-1
--# Var2 = 所要開啟的場景配置區ID-2
--# Var3 = 所要開啟的場景配置區ID-3
--# Var4 = 所要開啟的場景配置區ID-4
--# Var5 = 所要開啟的場景配置區ID-5
--# Var6 = 所要開啟的場景配置區ID-6
--# Var7 = 所要開啟的場景配置區ID-7
--# Var8 = 所要開啟的場景配置區ID-8
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Scene.PlacementON(Trigger.Var1);
  Scene.PlacementON(Trigger.Var2);
  Scene.PlacementON(Trigger.Var3);
  Scene.PlacementON(Trigger.Var4);
  Scene.PlacementON(Trigger.Var5);
  Scene.PlacementON(Trigger.Var6);
  Scene.PlacementON(Trigger.Var7);
  Scene.PlacementON(Trigger.Var8);
  Trigger.NextStatus();
  return 1

end