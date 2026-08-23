--# Var1 = 給予玩家道具的ID
--# Var2 = 道具最多持有數量
--# Var4 = 要檢查生或死怪物的配置區ID

function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var1);
  local M = Scene.CheckPlacementAlive(Trigger.Var4);

  if(I >= Trigger.Var2)then
    Player.ShowMessage(855)
    return 0
  elseif(M == true)then
    return 0
  else
  Player.AddItem(Trigger.Var1,1)
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
  end
end