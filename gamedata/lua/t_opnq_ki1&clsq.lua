--# Var1 = 在此機關開啟&完成的任務
--# Var2 = 開啟任務所需要的道具ID(鑰匙)
--# Var3 = 開啟任務所需要道具的數量
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local Q = Quest.GetQuestFlag(Trigger.Var1);
  local I = Player.GetItemNum(Trigger.Var2);

  if((Q == 0)and(I == Trigger.Var3))then
  Trigger.QuestActiveProgress(Trigger.Var1);
  Trigger.NextStatus();
    return 1

  elseif(Q == 1)then
  Trigger.QuestFinishProgress(Trigger.Var1);
  Trigger.NextStatus();
    return 1

  else
    return 0
  end
end