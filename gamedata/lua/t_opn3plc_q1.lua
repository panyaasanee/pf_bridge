--# Var1 = 所要開啟的場景配置區ID-1
--# Var2 = 所要開啟的場景配置區ID-2
--# Var3 = 所要開啟的場景配置區ID-3
--# Var4 = 所要檢查的任務ID
--# Var5 = 所檢查任務的旗標值

function ScriptStart()

  local Q = Quest.GetQuestFlag(Trigger.Var4);

  if (Q ~= Trigger.Var5) then
    return 0

  else
  Scene.PlacementON(Trigger.Var1);
  Scene.PlacementON(Trigger.Var2);
  Scene.PlacementON(Trigger.Var3);
  Trigger.NextStatus();
    return 1
  end
end