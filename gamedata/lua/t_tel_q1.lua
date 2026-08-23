--# Var1 = 傳送目標Marker點
--# Var2 = 所要檢查的任務ID-1
--# Var3 = 需要符合任務的旗標值
--# Var4 = 將玩家的重生點設為此Marker點


function ScriptStart()
	if(Quest.GetQuestFlag(Trigger.Var2) ~= Trigger.Var3)then
		return 0
	else
		Player.ResetMarker(Trigger.Var4);  
		Player.Teleport(Trigger.Var1);
		return 1
	end
end  