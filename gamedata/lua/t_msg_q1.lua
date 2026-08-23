--# Var1 = 所要判定的任務
--# Var2 = 對應系統訊息
--# Var3 = 判定的任務旗標

function ScriptStart()--指定任務未接時, 強制該任務完成;不會觸發完成對話
	if (Quest.GetQuestFlag(Trigger.Var1)==(Trigger.Var3))then
		Player.ShowMessage(Trigger.Var2)
		return 1
	end
end