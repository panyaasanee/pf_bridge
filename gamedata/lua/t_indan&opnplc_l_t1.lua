--# Var1 = 要受控制機關的ID
--# Var2 = 受控制機關的初始狀態
--# Var3 = 機關動態起始Frame
--# Var4 = 機關動態結束Frame
--# Var5 = 受控制機關的作用後狀態
--# Var6 = 要開啟的怪物配置區
--# Var7 = 另外要檢查的機關ID
--# Var8 = 要檢查機關的狀態

function ScriptStart()
  local S1 = Trigger.GetTriggerStatus(Trigger.Var1);
  local S2 = Trigger.GetTriggerStatus(Trigger.Var7);
  if(S1 ~= Trigger.Var2)or(S2 ~= Trigger.Var8)then
    return 0
  
  else
  Trigger.StartTriggerAnimation(Trigger.Var1,Trigger.Var3,Trigger.Var4,1); 
  Trigger.SetTriggerStatus(Trigger.Var1,Trigger.Var5);
  Scene.PlacementON(Trigger.Var6);
  Trigger.NextStatus()
    return 1
  end
end