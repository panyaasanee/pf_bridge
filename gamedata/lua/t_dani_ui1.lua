--# Var1 = 動態起始Frame
--# Var2 = 動態結束Frame
--# Var3 = 需求並扣除道具ID
--# Var4 = 需求並扣除道具數量
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var3);
  
  if(I < Trigger.Var4)then
    return 0  

  else
  Trigger.StartAnimation(Trigger.Var1,Trigger.Var2,1,1); 
  Player.RemoveItem(Trigger.Var3,Trigger.Var4);
  Trigger.NextStatus();
    return 1
  end;
end