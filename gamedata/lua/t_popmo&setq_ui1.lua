--# Var1 = 所要呼叫的怪物群組
--# Var2 = 所呼叫怪物隊伍的位置(MarkerID)
--# Var3 = 所要檢查並扣除道具的ID
--# Var4 = 所要檢查並扣除道具的數量
--# Var5 = 要改變旗標的任務ID
--# Var6 = 指定的任務旗標值
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var3)
  if(I < Trigger.Var4)then
    return 0
  
  else
  Player.RemoveItem(Trigger.Var3,Trigger.Var4);
  Mob.CallMob(Trigger.Var1,Trigger.Var2);
  Quest.SetQuestFlag(Trigger.Var5,Trigger.Var6)  
  Trigger.NextStatus();  
    return 1
  end
end