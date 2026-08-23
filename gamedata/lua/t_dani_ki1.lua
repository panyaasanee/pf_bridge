--# Var1 = 動態起始Frame
--# Var2 = 動態結束Frame
--# Var3 = 需要道具(鑰匙)ID
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var3);
  if(I == 0)then
    return 0  
  else
  Trigger.StartAnimation(Trigger.Var1,Trigger.Var2,1,1); 
    return 1
  end;
end