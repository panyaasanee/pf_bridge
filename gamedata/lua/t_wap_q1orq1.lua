--# Var1 = 瞬移目標點X值
--# Var2 = 瞬移目標點Y值
--# Var3 = 瞬移目標點Z值
--# Var4 = 面向(1~12)
--# Var5 = 所要檢查的任務ID-1
--# Var6 = 所要檢查的任務ID-2
--# Var7 = 需要檢查任務的旗標值
--# Var8 = 控制角色鏡頭面向
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local Q1 = Quest.GetQuestFlag(Trigger.Var5);
  local Q2 = Quest.GetQuestFlag(Trigger.Var6);
  if(Q1 == Trigger.Var7)or(Q2 == Trigger.Var7)then
    return 0

  else
  Player.CameraFocus(Trigger.Var8)
  Player.Warp(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);
    return 1
  end
end