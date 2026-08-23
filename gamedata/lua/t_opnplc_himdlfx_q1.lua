--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 所要檢查任務的ID
--# Var3 = 所要檢查任務的旗標值

function ScriptStart()
	if(Quest.GetQuestFlag(Trigger.Var2) ~= Trigger.Var3)then
		Player.ShowMessage(856) 
		return 0
	else
		Scene.PlacementON(Trigger.Var1);
		Trigger.HideModel();
		Trigger.PlayFx("S_HIT_FIREARM_FIRECROWN.fxs");
		Trigger.NextStatus();
		return 1
	end
end