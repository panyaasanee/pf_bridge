--# Var1 = 所要檢查的任務ID-1
--# Var2 = 所要檢查的任務ID-2
--# Var3 = 任務1旗標不能為
--# Var4 = 任務2旗標不能為
--# Var5 = 所要產生的副本

function ScriptStart()

  local Q1 = Quest.GetQuestFlag(Trigger.Var1);
  local Q2 = Quest.GetQuestFlag(Trigger.Var2);

  if(Q1 == Trigger.Var3)or(Q2 == Trigger.Var4) then
    return 0

  else
  Player.EnterInstance(Trigger.Var5);
  Trigger.NextStatus();
    return 1
  end
end
