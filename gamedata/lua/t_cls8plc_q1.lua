--# Var1 = 所要關閉的配置區ID-1
--# Var2 = 所要關閉的配置區ID-2
--# Var3 = 所要關閉的配置區ID-3
--# Var4 = 所要關閉的配置區ID-4
--# Var5 = 所要關閉的配置區ID-5
--# Var6 = 所要關閉的配置區ID-6
--# Var7 = 所要關閉的配置區ID-7
--# Var8 = 所要關閉的配置區ID-8
--# Var9 = 所要檢查的任務ID
--# Var10 = 任務必須要符合的旗標值
--# Var11 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local Q = Quest.GetQuestFlag(Trigger.Var9);

  if(Q ~= Trigger.Var10)then
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