--# Var1 = 所要檢查的任務ID
--# Var2 = 任務必須要符合的旗標值
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local Q = Quest.GetQuestFlag(Trigger.Var1);

  if(Q ~= Trigger.Var2)then
    return 0

  else
  Player.LeaveInstance();
    return 1
  end
end