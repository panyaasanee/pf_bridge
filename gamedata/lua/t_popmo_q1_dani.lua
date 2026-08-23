--# Var1 = 所要呼叫的怪物群組
--# Var2 = 所呼叫怪物隊伍的位置(MarkerID)
--# Var3 = 所要檢查任務的ID
--# Var4 = 所要檢查任務的旗標值
--# Var5 = 動態起始Frame
--# Var6 = 動態結束Frame


function ScriptStart()
  local Q = Quest.GetQuestFlag(Trigger.Var3);
  if(Q ~= Trigger.Var4)then
    return 0
  else
  Mob.CallMob(Trigger.Var1,Trigger.Var2);
  Trigger.StartAnimation(Trigger.Var5,Trigger.Var6,1,1); 
  Trigger.NextStatus();  
    return 1
  end
end