--# Var1 = 所要檢查的任務ID-1
--# Var2 = 所要檢查的任務ID-2
--# Var3 = 所要檢查的任務ID-3
--# Var4 = 任務必須要符合的旗標值
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local Q1 = Quest.GetQuestFlag(Trigger.Var1);
  local Q2 = Quest.GetQuestFlag(Trigger.Var2);
  local Q3 = Quest.GetQuestFlag(Trigger.Var3);
  if(Q1 ~= Trigger.Var4)and(Q2 ~= Trigger.Var4)and(Q3 ~= Trigger.Var4)then
    return 0

  else
  Player.LeaveInstance();
    return 1
  end
end