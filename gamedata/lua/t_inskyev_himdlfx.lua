--# Var1 = 觸發機關所獲得的關鍵事件次數

function ScriptStart()

  Instance.AddKeyEvent(Trigger.Var1)
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
  return 1
end