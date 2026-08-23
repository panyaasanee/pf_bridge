--# Var1 = 填入影片ID
--# Var2 = 播完影片後要進入的副本
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Player.EnterInstanceThenPlayMovie(Trigger.Var2,Trigger.Var1)

  return 1

end