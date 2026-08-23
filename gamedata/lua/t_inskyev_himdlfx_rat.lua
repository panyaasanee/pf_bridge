--# Var1 = 觸發機關所獲得的關鍵事件次數
--# Var3 = 觸發機關獲得關鍵事件計數的機率
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  if(not rate(Trigger.Var3))then
    return 0

  else
  Instance.AddKeyEvent(Trigger.Var1)
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
  end
end