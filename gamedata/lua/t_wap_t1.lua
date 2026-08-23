--# Var1 = 瞬移目標點X值
--# Var2 = 瞬移目標點Y值
--# Var3 = 瞬移目標點Z值
--# Var4 = 面向(1~12)
--# Var5 = 前置機關ID
--# Var6 = 前置機關要符合的狀態

function ScriptStart()

  local T = Trigger.GetTriggerStatus(Trigger.Var5);
  
  if (T == Trigger.Var6) then
    return 0

  else
  Player.Warp(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);
    return 1
  end
end