--# Var1 = 等級在幾級以上才會觸發
--# Var2 = 三個副本共用的觸發機率
--# Var3 = 可能觸發的副本-1
--# Var4 = 可能觸發的副本-2
--# Var5 = 可能觸發的副本-3
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local L = Player.GetLv();
  if(L < Trigger.Var1)then
    return 0 

  elseif rate(Trigger.Var2)then 
  Player.EnterInstance(Trigger.Var3);
  Trigger.NextStatus();
    return 1

  elseif rate(Trigger.Var2)then 
  Player.EnterInstance(Trigger.Var4);
  Trigger.NextStatus();
    return 1

  elseif rate(Trigger.Var2)then 
  Player.EnterInstance(Trigger.Var5);
  Trigger.NextStatus();
    return 1

  else
  Trigger.NextStatus();
    return 1
  end
end
