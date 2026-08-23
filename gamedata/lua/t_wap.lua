--# Var1 = 瞬移目標點X值
--# Var2 = 瞬移目標點Y值
--# Var3 = 瞬移目標點Z值
--# Var4 = 面向(1~12)

function ScriptStart()

  Player.Warp(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);
  return 1

end