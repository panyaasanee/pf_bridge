--# Var1 = 所要執行的掉落群
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Player.DropProcess(Trigger.Var1);
  Trigger.NextStatus();
  return 1

end