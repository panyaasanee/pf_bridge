--# Var1 = 瞬移目標點X值
--# Var2 = 瞬移目標點Y值
--# Var3 = 瞬移目標點Z值
--# Var4 = 面向(1~12)
--# Var5 = 所要檢查的機關ID
--# Var6 = 未使用
--# Var7 = 需要檢查機關的狀態值
--# Var8 = 控制角色鏡頭面向
--# Var9 = 上BUFF的ID
--# Var10 = BUFF標準等級
--# Var11 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local T = Quest.GetQuestFlag(Trigger.Var5);
  if(T == Trigger.Var7)then
    return 0

  else
  Player.CameraFocus(Trigger.Var8);
  Player.AddBuff(Trigger.Var9,Trigger.Var10);
  Player.Warp(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);
    return 1
  end
end