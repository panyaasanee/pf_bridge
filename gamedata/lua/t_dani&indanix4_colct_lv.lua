--# Var1 = 直接受控制機關的ID
--# Var2 = 間接受控制機關1的ID
--# Var3 = 間接受控制機關2的ID
--# Var4 = 間接受控制機關3的ID
--# Var5 = 間接受控制機關4的ID
--# Var6 = 所有受控制機關的初始狀態
--# Var7 = 所要檢查的圖鑑ID
--# Var8 = 操作者限制等級
--# Var9 = 直接控制物件的動態起始Frame
--# Var10 = 直接控制物件的動態結束Frame
--# Var11 = 間接控制物件的動態結束Frame
--# Var12 = 間接控制物件的動態結束Frame
--# Var13 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local S1 = Trigger.GetTriggerStatus(Trigger.Var1);
  local S2 = Trigger.GetTriggerStatus(Trigger.Var2);
  local S3 = Trigger.GetTriggerStatus(Trigger.Var3);
  local S4 = Trigger.GetTriggerStatus(Trigger.Var4);
  local S5 = Trigger.GetTriggerStatus(Trigger.Var5);
  local L = Player.GetLv();
  local C = Player.CheckCollect(Trigger.Var7);

  if((S1 ~= Trigger.Var6) or (S2 ~= Trigger.Var6) or (S3 ~= Trigger.Var6) or (S4 ~= Trigger.Var6) or (S5 ~= Trigger.Var6) or (L < Trigger.Var8) or (C ~= true))then
    return 0

  else
  Trigger.StartTriggerAnimation(Trigger.Var2,Trigger.Var11,Trigger.Var12,1);  
  Trigger.StartTriggerAnimation(Trigger.Var3,Trigger.Var11,Trigger.Var12,1);  
  Trigger.StartTriggerAnimation(Trigger.Var4,Trigger.Var11,Trigger.Var12,1);  
  Trigger.StartTriggerAnimation(Trigger.Var5,Trigger.Var11,Trigger.Var12,1);   
  Trigger.StartAnimation(Trigger.Var9,Trigger.Var10,1); 
  Trigger.NextStatus();
    return 1
  end
end