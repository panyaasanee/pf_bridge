--# Var1 = 所要觸發的任務

function ScriptStart()
  local Q = Quest.GetQuestFlag(Trigger.Var1);
  if(Q ~= 0)then
    return 0

  else
  Trigger.QuestActiveProgress(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end