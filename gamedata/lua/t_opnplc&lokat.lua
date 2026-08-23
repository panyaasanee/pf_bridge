--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 控制角色鏡頭面向
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Scene.PlacementON(Trigger.Var1);
  Player.CameraFocus(Trigger.Var2);
  Trigger.NextStatus();
  return 1

end