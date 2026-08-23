--# Var1 = 所要檢查任務的ID
--# Var2 = 所要檢查任務的旗標值
--# Var3 = 跳出的教學界面

function ScriptStart()
	if(Quest.GetQuestFlag(Trigger.Var1) ~= Trigger.Var2)then
		return 0
	else
		Player.OpenHelpUI(Trigger.Var3)
		Trigger.NextStatus();
		return 1
	end
end