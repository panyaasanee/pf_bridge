--# Var1 = 給予玩家道具的ID
--# Var2 = 道具最多持有數量
--# Var3 = 所要檢查任務的ID
--# Var4 = 所要檢查任務的旗標值
--# Var5 = 檢查場景上是否存在此ID的怪物
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var1);
  local Q = Quest.GetQuestFlag(Trigger.Var3);
  local M = Mob.CheckMobalive(Trigger.Var5);  

  if(I >= Trigger.Var2)or(Q ~= Trigger.Var4)or(M == false)then
    return 0

  else
  Player.AddItem(Trigger.Var1,1)
  Trigger.NextStatus();
    return 1
  end
end