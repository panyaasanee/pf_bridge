--# Var1 = 所要檢查的機關ID
--# Var2 = 玩家身上需要攜帶&領完移除的BUFF
--# Var3 = 機關需要符合的狀態
--# Var4 = 要給予玩家的道具
--# Var5 = 3V3沙灘足球專用

function ScriptStart()
  local T = Trigger.GetTriggerStatus(Trigger.Var1);
  local B = Player.CheckBuff(Trigger.Var2);
  
  if((T ~= Trigger.Var3)or(B == false))then
    return 0

  else
  Player.AddItem(Trigger.Var4,1)
  Player.RemoveBuff(Trigger.Var2)
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
  end
end