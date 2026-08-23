--# Var1 = 要對觸發者施放的技能
--# Var2 = 所要檢查任務的ID
--# Var3 = 所要檢查任務的旗標值
--# Var4 = 動態起始Frame
--# Var5 = 動態結束Frame

function ScriptStart()
  local Q = Quest.GetQuestFlag(Trigger.Var2);
  if(Q ~= Trigger.Var3)then
    Player.ShowMessage(856) 
    return 0
  else
  Player.CastSkillAt(Trigger.Var1);
  Trigger.StartAnimation(Trigger.Var4,Trigger.Var5,1); 
  Trigger.NextStatus();
    return 1
  end
end