--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 所要檢查任務的ID
--# Var3 = 所要檢查任務的旗標值

function ScriptStart()
  local Q = Quest.GetQuestFlag(Trigger.Var2);
  if(Q ~= Trigger.Var3)then
    return 0

  else
  Scene.PlacementON(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end