--# Var1 = 動態起始Frame
--# Var2 = 動態結束Frame
--# Var3 = 所要檢查機關的ID
--# Var4 = 所要檢查機關的狀態

function ScriptStart()
  local S = Trigger.GetTriggerStatus(Trigger.Var3);
  
  if(S ~= Trigger.Var4)then
    return 0  
  else
  Trigger.StartAnimation(Trigger.Var1,Trigger.Var2,1); 
  Trigger.NextStatus();
    return 1
  end;
end