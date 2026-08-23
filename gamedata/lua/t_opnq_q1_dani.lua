--# Var1 = 所要觸發的任務
--# Var2 = 要檢查任務的ID
--# Var3 = 要檢查任務的旗標值
--# Var4 = 動態起始Frame
--# Var5 = 動態結束Frame
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local Q1 = Quest.GetQuestFlag(Trigger.Var1);
  local Q2 = Quest.GetQuestFlag(Trigger.Var2);
  if(Q1 ~= 0)then
    return 0
  elseif(Q2 ~= Trigger.Var3)then
    return 0

  else
  Trigger.QuestActiveProgress(Trigger.Var1);
  Trigger.StartAnimation(Trigger.Var4,Trigger.Var5,1,1); 
  Trigger.NextStatus();
    return 1
  end
end