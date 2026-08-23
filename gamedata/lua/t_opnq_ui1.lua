--# Var1 = 所要觸發的任務
--# Var2 = 所需要並扣除的道具ID
--# Var3 = 所需要並扣除的道具數量
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local Q = Quest.GetQuestFlag(Trigger.Var1);
  local I = Player.GetItemNum(Trigger.Var2);
  if(Q ~= 0)then
    return 0
  elseif(I < Trigger.Var3)then
    return 0

  else
  Player.RemoveItem(Trigger.Var2,Trigger.Var3);
  Trigger.QuestActiveProgress(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end