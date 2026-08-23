--# Var1 = 得到道具2的機率
--# Var2 = 給予道具1的ID
--# Var3 = 給予道具2的ID
--# Var4 = 給予道具1&2的數量

function ScriptStart()

  if(not rate(Trigger.Var1))then 
  Player.AddItem(Trigger.Var2,Trigger.Var4);
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1

  else
  Player.AddItem(Trigger.Var3,Trigger.Var4);
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
  end
end