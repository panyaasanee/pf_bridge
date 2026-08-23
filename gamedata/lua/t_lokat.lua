--# Var1 = 控制角色鏡頭面向
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Player.CameraFocus(Trigger.Var1);
  Trigger.NextStatus();
  return 1

end