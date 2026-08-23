--# Var1 = 直接控制物件的動態起始Frame
--# Var2 = 直接控制物件的動態結束Frame
--# Var3 = 間接控制物件的綁定機關ID
--# Var4 = 間接控制物件的動態起始Frame
--# Var5 = 間接控制物件的動態結束Frame
--# Var6 = 要扣除道具的ID
--# Var7 = 要扣除道具的數量

function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var6);
  
  if(I < Trigger.Var7)then
    return 0  

  else
  Trigger.StartTriggerAnimation(Trigger.Var3,Trigger.Var4,Trigger.Var5,1,1);   
  Trigger.StartAnimation(Trigger.Var1,Trigger.Var2,1,1);
  Player.RemoveItem(Trigger.Var6,Trigger.Var7); 
  Trigger.NextStatus()
    return 1
  end
end