--# Var1 = 所要控制機關的ID
--# Var2 = 所要控制機關的初始狀態
--# Var3 = 所要控制機關的指定狀態
--# Var4 = 所要檢查的任務ID
--# Var5 = 所要檢查任務的旗標值
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local S = Trigger.GetTriggerStatus(Trigger.Var1);
  local Q = Quest.GetQuestFlag(Trigger.Var4);
  if(S ~= Trigger.Var2)or(Q == Trigger.Var5)then
    return 0

  else
  Trigger.SetTriggerStatus(Trigger.Var1,Trigger.Var3);
  Trigger.NextStatus();
    return 1
  end
end