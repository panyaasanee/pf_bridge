--# Var1 = 在此機關開啟&完成的任務


function ScriptStart()
  local Q = Quest.GetQuestFlag(Trigger.Var1);

  if(Q == 0)then
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