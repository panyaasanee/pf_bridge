--# Var1 = 玩家藉由機關所要施放的技能

function ScriptStart()

	Trigger.CastSkill(Trigger.Var1);
	Trigger.HideModel();
	Trigger.NextStatus();
	return 1
end