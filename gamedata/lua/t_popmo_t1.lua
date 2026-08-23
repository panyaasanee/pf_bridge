--# Var1 = 所要呼叫的怪物群組
--# Var2 = 所呼叫怪物隊伍的位置(MarkerID)
--# Var3 = 所要檢查機關的ID
--# Var4 = 所要檢查機關的狀態
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local S = Trigger.GetTriggerStatus(Trigger.Var3);
  if(S ~= Trigger.Var4)then
    return 0

  else
  Mob.CallMob(Trigger.Var1,Trigger.Var2);
  Trigger.NextStatus();  
    return 1
  end
end