--# Var1 = 直接控制物件的動態起始Frame
--# Var2 = 直接控制物件的動態結束Frame
--# Var3 = 間接控制物件的綁定機關ID
--# Var4 = 間接控制物件的動態結束Frame
--# Var5 = 間接控制物件的動態結束Frame

function ScriptStart()

  Trigger.StartTriggerAnimation(Trigger.Var3,Trigger.Var4,Trigger.Var5,1,1);   
  Trigger.StartAnimation(Trigger.Var1,Trigger.Var2,1,1); 
  Trigger.NextStatus()
    return 1
end