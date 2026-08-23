--# Var1 = 所要開啟的場景配置區ID-1
--# Var2 = 所要開啟的場景配置區ID-2
--# Var3 = 所要開啟的場景配置區ID-3
--# Var4 = 所要開啟的場景配置區ID-4
--# Var5 = 所要開啟的場景配置區ID-5
--# Var6 = 所要開啟的場景配置區ID-6
--# Var7 = 所要開啟的場景配置區ID-7
--# Var8 = 所要開啟的場景配置區ID-8
--# Var9 = 所要檢查的任務ID-1
--# Var10 = 所要檢查的任務ID-2
--# Var11 = 所要檢查的任務ID-3
--# Var12 = 所要檢查的任務ID-4
--# Var13 = 任務必須要符合的旗標值

function ScriptStart()

  local Q1 = Quest.GetQuestFlag(Trigger.Var9);
  local Q2 = Quest.GetQuestFlag(Trigger.Var10);
  local Q3 = Quest.GetQuestFlag(Trigger.Var11);
  local Q4 = Quest.GetQuestFlag(Trigger.Var12);
  if(Q1 ~= Trigger.Var13)and(Q2 ~= Trigger.Var13)and(Q3 ~= Trigger.Var13)and(Q4 ~= Trigger.Var13)then
    return 0
  
  else
  Scene.PlacementON(Trigger.Var1);
  Scene.PlacementON(Trigger.Var2);
  Scene.PlacementON(Trigger.Var3);
  Scene.PlacementON(Trigger.Var4);
  Scene.PlacementON(Trigger.Var5);
  Scene.PlacementON(Trigger.Var6);
  Scene.PlacementON(Trigger.Var7);
  Scene.PlacementON(Trigger.Var8);
  Trigger.NextStatus();
    return 1
  end
end