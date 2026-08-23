--# Var1 = 玩家藉由機關所要施放的技能
--# Var2 = 技能所指向的座標點X值
--# Var3 = 技能所指向的座標點Y值
--# Var4 = 技能所指向的座標點Z值
--# Var5 = 所要檢查的任務ID-1
--# Var6 = 所要檢查的任務ID-2
--# Var7 = 需要符合任務的旗標值
--# Var8 = 控制角色鏡頭面向哪個方向(1~12)

function ScriptStart()
  local Q1 = Quest.GetQuestFlag(Trigger.Var5);
  local Q2 = Quest.GetQuestFlag(Trigger.Var6);
  if(Q1 ~= Trigger.Var7)and(Q2 ~= Trigger.Var7)then
    Player.ShowMessage(856)  
    return 0
  else
  Player.CameraFocus(Trigger.Var8)
  Trigger.CastSkillXYZ(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);
  Trigger.NextStatus();
    return 1
  end
end