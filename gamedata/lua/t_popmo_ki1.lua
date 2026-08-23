--# Var1 = 所要呼叫的怪物群組
--# Var2 = 所呼叫怪物隊伍的位置(MarkerID)
--# Var3 = 需求道具的ID(鑰匙)
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var3);
  if(I == 0)then
    return 0

  else
  Mob.CallMob(Trigger.Var1,Trigger.Var2);
  Trigger.NextStatus();  
    return 1
  end
end