--# Var1 = 觸發機關所獲得的關鍵事件次數

function ScriptStart()

  Instance.AddKeyEvent(Trigger.Var1);
  Trigger.NextStatus();
  return 1

end