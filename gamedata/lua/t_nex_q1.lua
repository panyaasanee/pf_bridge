--# Var1 = 所要檢查任務的ID
--# Var2 = 所要檢查任務的旗標值
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

local Q = Quest.GetQuestFlag(Trigger.Var1);
  if(Q ~= Trigger.Var2)then
    return 0

  else
  Trigger.NextStatus();
    return 1
  end
end