--# Var1 = 所要執行的掉落群
--# Var2 = 所要檢查的任務ID
--# Var3 = 所要檢查的任狀態
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
local Q = Quest.GetQuestFlag(Trigger.Var2);
  if(Q ~= Trigger.Var3)then
    return 0
  else
  Player.DropProcess(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end