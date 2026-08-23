--# Var1 = Ι埃笵ㄣID
--# Var2 = Ι埃笵ㄣ计秖
--# Var3 = 传莉眔笵ㄣID
--# Var4 = 传莉眔笵ㄣ计秖

function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var1)
  if(I < Trigger.Var2)then
    Player.ShowMessage(859)
    return 0
  else
  Player.RemoveItem(Trigger.Var1,Trigger.Var2);
  Player.AddItem(Trigger.Var3,Trigger.Var4);
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
  end
end