--# Var1 = 海神島海魅影戰鬥配樂專用

function ScriptStart()
	if(Scene.CheckPlacementAlive(18) == true)then
		return 0
	else
		Scene.ChangeMainMusic("Scn4003")
		Trigger.NextStatus();
		return 1
	end
end