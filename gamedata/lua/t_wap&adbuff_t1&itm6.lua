--# Var1 = 瞬移目標點X值
--# Var2 = 瞬移目標點Y值
--# Var3 = 瞬移目標點Z值
--# Var4 = 面向(1~12)
--# Var5 = 所要檢查的機關ID
--# Var6 = 需要檢查機關的狀態值
--# Var7 = 控制角色鏡頭面向
--# Var8 = 上BUFF的ID
--# Var9 = BUFF標準等級
--# Var10 = 檢驗身上有無道具ID-1
--# Var11 = 檢驗身上有無道具ID-2
--# Var12 = 檢驗身上有無道具ID-3
--# Var13 = 檢驗身上有無道具ID-4
--# Var14 = 檢驗身上有無道具ID-5
--# Var15 = 檢驗身上有無道具ID-6

function ScriptStart()

  local T = Trigger.GetTriggerStatus(Trigger.Var5);
  local I1 = Player.GetItemNum(Trigger.Var10);
  local I2 = Player.GetItemNum(Trigger.Var11);  
  local I3 = Player.GetItemNum(Trigger.Var12);  
  local I4 = Player.GetItemNum(Trigger.Var13);  
  local I5 = Player.GetItemNum(Trigger.Var14);  
  local I6 = Player.GetItemNum(Trigger.Var15);  
  if(T == Trigger.Var6)or(I1 ~= 0) or (I2 ~= 0) or (I3 ~= 0) or (I4 ~= 0) or (I5 ~= 0) or (I6 ~= 0)then
    return 0

  else
  Player.CameraFocus(Trigger.Var7);
  Player.AddBuff(Trigger.Var8,Trigger.Var9);
  Player.Warp(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);
    return 1
  end
end