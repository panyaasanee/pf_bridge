--# Var1 = 動態起始Frame
--# Var2 = 動態結束Frame

function ScriptStart()
  
  Trigger.StartAnimation(Trigger.Var1,Trigger.Var2,1,1); 
  Trigger.NextStatus()
    return 1
end