--# Var1 = 給予玩家道具的ID
--# Var2 = 道具最多持有數量
--# Var3 = 所要檢查機關的ID
--# Var4 = 所要檢查機關的狀態

function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var1);
  local S = Trigger.GetTriggerStatus(Trigger.Var3);

  if(I >= Trigger.Var2)then
    Player.ShowMessage(855)
    return 0
  elseif(S ~= Trigger.Var4)then
    return 0
  else
  Player.AddItem(Trigger.Var1,1)
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
  end
end