--# Var1 = 副本剩餘時間低於多少秒

function ScriptStart()

  local T = Instance.GetLastingTime();
  if (T > Trigger.Var1)then
    return 0
  else
  Trigger.NextStatus();
    return 1
  end
end