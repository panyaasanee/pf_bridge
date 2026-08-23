--# Var1 = 觸發機關所扣除的關鍵事件次數
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Instance.RemoveKeyEvent(Trigger.Var1);
  Trigger.NextStatus();
  return 1

end