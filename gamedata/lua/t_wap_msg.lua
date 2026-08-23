--# Var1 = 瞬移目標點X值
--# Var2 = 瞬移目標點Y值
--# Var3 = 瞬移目標點Z值
--# Var4 = 面向(1~12)
--# Var5 = 顯示訊息編號

function ScriptStart()

  Player.Warp(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);
  Player.ShowMessage(Trigger.Var5)
  return 1

end