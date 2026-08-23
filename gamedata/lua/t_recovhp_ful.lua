--# Var1 = 回復多少百分比的血量
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local HP1 = Player.GetMaxHP();
  local HP2 = Player.GetCurrentHP();
  if(HP1 == HP2)then
    return 0
  else
  Player.AddHP(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end