--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 所要檢查任務的ID-1
--# Var3 = 所要檢查任務的旗標值
--# Var4 = 所要檢查任務的ID-2

function ScriptStart()
  local Q1 = Quest.GetQuestFlag(Trigger.Var2);
  local Q2 = Quest.GetQuestFlag(Trigger.Var4);
  if(Q1 ~= Trigger.Var3)and(Q2 ~= Trigger.Var3)then
    return 0

  else
  Scene.PlacementON(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end