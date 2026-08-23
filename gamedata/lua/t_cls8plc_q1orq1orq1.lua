--# Var1 = 所要關閉的配置區ID-1
--# Var2 = 所要關閉的配置區ID-2
--# Var3 = 所要關閉的配置區ID-3
--# Var4 = 所要關閉的配置區ID-4
--# Var5 = 所要關閉的配置區ID-5
--# Var6 = 所要關閉的配置區ID-6
--# Var7 = 所要關閉的配置區ID-7
--# Var8 = 所要關閉的配置區ID-8
--# Var9 = 所要檢查的任務ID-1
--# Var10 = 所要檢查的任務ID-2
--# Var11 = 所要檢查的任務ID-3
--# Var12 = 任務必須要符合的旗標值
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local Q1 = Quest.GetQuestFlag(Trigger.Var9);
  local Q2 = Quest.GetQuestFlag(Trigger.Var10);
  local Q3 = Quest.GetQuestFlag(Trigger.Var11);
  if(Q1 ~= Trigger.Var12)and(Q2 ~= Trigger.Var12)and(Q3 ~= Trigger.Var12)then
    return 0

  else
  Scene.PlacementOFF(Trigger.Var1);
  Scene.PlacementOFF(Trigger.Var2);
  Scene.PlacementOFF(Trigger.Var3);
  Scene.PlacementOFF(Trigger.Var4);
  Scene.PlacementOFF(Trigger.Var5);
  Scene.PlacementOFF(Trigger.Var6);
  Scene.PlacementOFF(Trigger.Var7);
  Scene.PlacementOFF(Trigger.Var8);
  Trigger.NextStatus();
    return 1
  end
end