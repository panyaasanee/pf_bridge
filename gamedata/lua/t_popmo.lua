--# Var1 = 所要呼叫的怪物群組
--# Var2 = 所呼叫怪物隊伍的位置(MarkerID)
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Mob.CallMob(Trigger.Var1,Trigger.Var2);
  Trigger.NextStatus();  
  return 1
end