--# Var1 = 玩家藉由機關所要施放的技能
--# Var2 = 技能所指向的座標點X值
--# Var3 = 技能所指向的座標點Y值
--# Var4 = 技能所指向的座標點Z值
--# Var5 = 發動技能前瞬移行為的座標點X值
--# Var6 = 發動技能前瞬移行為的座標點Y值
--# Var7 = 發動技能前瞬移行為的座標點Z值
--# Var8 = 發動技能前瞬移行為的面向
--# Var9 = 發動機關不要錢

function ScriptStart()

	Player.Warp(Trigger.Var5,Trigger.Var6,Trigger.Var7,Trigger.Var8);
	Trigger.CastSkillXYZ(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);
	Trigger.NextStatus();
    return 1

end