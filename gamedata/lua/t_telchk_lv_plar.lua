--# Var1 = 傳送目標Marker點
--# Var2 = 等級限制

function ScriptStart()
  local L = Player.GetLv();

  if(L < Trigger.Var2)then
    return 0

  else
  Player.Teleport(Trigger.Var1);
    return 1
  end
end  