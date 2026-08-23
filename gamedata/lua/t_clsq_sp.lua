--# Var1 = 所要完結的任務
--# Var2 = 對應系統訊息
--# Var3 = 所要判斷的任務
--# Var4 = 所判斷任務的旗標

function ScriptStart()--指定任務為指定狀態時, 強制指定任務完成;不會觸發完成對話
	if (Quest.GetQuestFlag(Trigger.Var3)==Trigger.Var4)then
		if (Quest.GetQuestFlag(Trigger.Var1)==0)then
			Quest.SetQuestFlag(Trigger.Var1,2);
			Player.ShowMessage(Trigger.Var2)
			return 1
		end
	end
end