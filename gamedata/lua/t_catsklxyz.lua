--# Var1 = 玩家藉由機關所要施放的技能
--# Var2 = 技能所指向的座標點X值
--# Var3 = 技能所指向的座標點Y值
--# Var4 = 技能所指向的座標點Z值

function ScriptStart()
  
  Trigger.CastSkillXYZ(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);
  Player.OutVehicle()
  Trigger.NextStatus();
  return 1
end