--# Var1 = 傳送目標Marker點
--# Var2 = 所要檢查的任務ID-1
--# Var3 = 所要檢查的任務ID-2
--# Var4 = 需要符合任務的旗標值
--# Var5 = 所要檢查的任務ID-3
--# Var6 = 所要檢查的任務ID-4
--# Var7 = 將玩家的重生點設為此Marker點


function ScriptStart()
  local Q1 = Quest.GetQuestFlag(Trigger.Var2);
  local Q2 = Quest.GetQuestFlag(Trigger.Var3);
  local Q3 = Quest.GetQuestFlag(Trigger.Var5);
  local Q4 = Quest.GetQuestFlag(Trigger.Var6);
  if(Q1 ~= Trigger.Var4)and(Q2 ~= Trigger.Var4)and(Q3 ~= Trigger.Var4)and(Q4 ~= Trigger.Var4)then
    return 0

  else
  Player.ResetMarker(Trigger.Var7);  
  Player.Teleport(Trigger.Var1);
    return 1
  end
end  