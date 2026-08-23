--# Var1 = 觸發機關所獲得的關鍵事件次數
--# Var3 = 檢查死或活怪物的ID
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local M = Mob.CheckMobalive(Trigger.Var3);
  if(M == true)then
    return 0

  else
  Instance.AddKeyEvent(Trigger.Var1)
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
  end
end