--# Var1 = 所要開啟的場景配置區ID-1
--# Var2 = 所要開啟的場景配置區ID-2

function ScriptStart()

  Scene.PlacementON(Trigger.Var1);
  Scene.PlacementON(Trigger.Var2);
  Trigger.NextStatus();
   return 1

end