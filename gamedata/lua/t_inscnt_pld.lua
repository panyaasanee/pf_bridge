--# Var1 = 沒有變數、以下空白
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local L = Player.CheckPartyLeader();
  if (L == false)then
    return 0
  else
  Instance.CallScoreCount();
  Trigger.NextStatus();
    return 1
  end
end