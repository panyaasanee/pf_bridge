function ScriptStart()
--# Var9 = 2014-4-17開發版未使用-使用前需再check
  Player.AddItem(2600002,60)
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
end
