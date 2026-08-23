--# Var1 = 給予玩家道具的ID
--# Var2 = 道具最多持有數量
--# Var3 = 所要檢查任務的ID
--# Var4 = 所要檢查任務的旗標值

function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var1);
  local Q = Quest.GetQuestFlag(Trigger.Var3)

	if(I >= Trigger.Var2)then
		Player.ShowMessage(855)
		return 0	
	elseif(Q ~= Trigger.Var4)then
		Player.ShowMessage(856)
		return 0

	else
		Player.AddItem(Trigger.Var1,1)
		Trigger.HideModel();
		Trigger.PlayFx("BgFx0005_002.fxs");
		Trigger.NextStatus();
		return 1
	end
end