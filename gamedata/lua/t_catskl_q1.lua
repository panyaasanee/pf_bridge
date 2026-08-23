--# Var1 = 所要檢查的任務ID
--# Var2 = 所要檢查任務的旗標值
--# Var3 = 玩家藉由機關所要施放的技能

function ScriptStart()

  local Q = Quest.GetQuestFlag(Trigger.Var1);
  if(Q ~= Trigger.Var2)then
    Player.ShowMessage(856) 
    return 0
  else  
  Trigger.CastSkill(Trigger.Var3);
  Trigger.NextStatus();
    return 1
  end
end