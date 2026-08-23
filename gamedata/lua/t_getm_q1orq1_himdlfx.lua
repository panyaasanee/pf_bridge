--# Var1 = 給予玩家道具的ID
--# Var2 = 道具最多持有數量
--# Var3 = 所要檢查任務的ID-1
--# Var4 = 所要檢查任務的旗標值
--# Var5 = 同時要Hide掉的物件身上的TriggerID
--# Var6 = 所要檢查任務的ID-2

function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var1);
  local Q1 = Quest.GetQuestFlag(Trigger.Var3)
  local Q2 = Quest.GetQuestFlag(Trigger.Var6)

  if(I >= Trigger.Var2)then
    Player.ShowMessage(855) 
    return 0
  elseif(Q1 ~= Trigger.Var4)and(Q2 ~= Trigger.Var4)then
    Player.ShowMessage(856)  
    return 0

  else
  Player.AddItem(Trigger.Var1,1)
  Trigger.HideModel();
  Trigger.HideTriggerModel(Trigger.Var5);
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
  end
end