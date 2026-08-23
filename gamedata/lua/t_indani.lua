--# Var1 = 動態起始Frame
--# Var2 = 動態結束Frame
--# Var3 = 要受控制機關的ID
--# Var4 = 受控制機關的初始狀態
--# Var5 = 受控制機關的作用後狀態

function ScriptStart()
  local S = Trigger.GetTriggerStatus(Trigger.Var3);
  if(S ~= Trigger.Var4)then
    return 0
  
  else
  Trigger.StartTriggerAnimation(Trigger.Var3,Trigger.Var1,Trigger.Var2,1); 
  Trigger.SetTriggerStatus(Trigger.Var3,Trigger.Var5);
  Trigger.NextStatus()
    return 1
  end;
end