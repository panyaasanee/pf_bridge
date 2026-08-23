--# Var1 = 填入圖鑑ID
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Instance.AddBonusPoint(Trigger.Var1)
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");  
  Trigger.NextStatus();
  return 1

end