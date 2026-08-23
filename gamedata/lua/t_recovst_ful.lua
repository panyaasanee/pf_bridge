--# Var1 = 回復多少百分比的精力值
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local ST1 = Player.GetMaxST();
  local ST2 = Player.GetCurrentST();
  if(ST1 == ST2)then
    return 0
  else
  Player.AddST(Trigger.Var1);
  Trigger.NextStatus();
    return 1
  end
end