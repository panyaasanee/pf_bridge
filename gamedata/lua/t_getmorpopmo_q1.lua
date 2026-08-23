--# Var1 = 給予玩家道具的ID
--# Var2 = 道具最多持有數量
--# Var3 = 所要檢查任務的ID
--# Var4 = 所要檢查任務的旗標值
--# Var5 = 產生怪物的機率
--# Var6 = 所要呼叫的怪物群組
--# Var7 = 所呼叫怪物隊伍的位置(MarkerID)
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var1);
  local Q = Quest.GetQuestFlag(Trigger.Var3);

  if((I >= Trigger.Var2)or(Q ~= Trigger.Var4))then
    return 0
  end

  if(rate(Trigger.Var5)) then
    Mob.CallMob(Trigger.Var6,Trigger.Var7);
    Trigger.NextStatus();  
    return 1
  else
    Player.AddItem(Trigger.Var1,1)
    Trigger.NextStatus();
    return 1
  end
end