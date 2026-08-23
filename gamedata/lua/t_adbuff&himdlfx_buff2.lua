--# Var1 = 身上不能有的BUFF-1
--# Var2 = 身上不能有的BUFF-2
--# Var3 = 被強制施加的BUFF
--# Var4 = BUFF標準等級
--# Var5 = 要隱藏的機關ID

function ScriptStart()

  local B1 = Player.CheckBuff(Trigger.Var1)
  local B2 = Player.CheckBuff(Trigger.Var2)
  
  if (B1 == true)or(B2 == true)then
    return 0
	
  else
  Player.AddBuff(Trigger.Var3,Trigger.Var4);
   Player.AddAndEquip(2209905,8)
  Trigger.HideModel();
  Trigger.HideTriggerModel(Trigger.Var5);
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
  end
end