--# Var1 = 給予玩家道具的ID
--# Var2 = 道具最多持有數量
--# Var3 = 取得道具同時放一個技能ID

function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var1);
  if(I >= Trigger.Var2)then
    Player.ShowMessage(855)
    return 0
  else
  Player.AddItem(Trigger.Var1,1)
  Trigger.CastSkill(Trigger.Var3);
  Trigger.PlayFx("Fx_bgs0064.fxs");
  Trigger.NextStatus();
    return 1
  end
end