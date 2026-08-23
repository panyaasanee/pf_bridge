--# Var1 = 所要完結的任務

function ScriptStart()
  local Q = Quest.GetQuestFlag(Trigger.Var1);
  if(Q ~= 1)then
    return 0

  else
  Trigger.QuestFinishProgress(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end