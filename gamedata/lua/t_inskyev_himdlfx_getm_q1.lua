--# Var1 = 觸發機關所獲得的關鍵事件次數
--# Var3 = 要檢查的任務
--# Var4 = 要檢查的任務旗標
--# Var5 = 若任務己查通過，額外獲得的道具ID
--# Var6 = 若任務己查通過，額外獲得的道具數量
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

local Q = Quest.GetQuestFlag(Trigger.Var3);
  if(Q ~= Trigger.Var4)then
  Instance.AddKeyEvent(Trigger.Var1)
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1

  else
  Player.AddItem(Trigger.Var5,Trigger.Var6);
  Instance.AddKeyEvent(Trigger.Var1)
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
  end
end