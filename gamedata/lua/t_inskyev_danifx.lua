--# Var1 = 動態起始Frame
--# Var2 = 動態結束Frame
--# Var4 = 觸發機關所獲得的關鍵事件次數
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Trigger.StartAnimation(Trigger.Var1,Trigger.Var2,1,Once);
  Trigger.PlayFx("BgFx0005_002.fxs");
  Instance.AddKeyEvent(Trigger.Var4);
  Trigger.NextStatus();

end