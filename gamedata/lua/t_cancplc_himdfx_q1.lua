--# Var1 = 所要關閉的配置區ID
--# Var2 = 所要檢查任務的ID
--# Var3 = 所要檢查任務的旗標值

function ScriptStart()

 local Q = Quest.GetQuestFlag(Trigger.Var2);
  if(Q ~= Trigger.Var3)then
    Player.ShowMessage(856) 
    return 0
  else
  Scene.PlacementCancel(Trigger.Var1);
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
  end
end