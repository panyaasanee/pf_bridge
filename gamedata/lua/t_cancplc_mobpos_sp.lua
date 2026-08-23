--# Var1 = 所要回收的場景配置區ID
--# Var2 = 要檢查的怪物ID
--# Var3 = 中心點座標X1
--# Var4 = 中心點座標Y1
--# Var5 = 中心點座標Z1
--# Var6 = 中心點座標X2
--# Var7 = 中心點座標Y2
--# Var8 = 中心點座標Z2
--# Var9 = 中心點座標X3
--# Var10 = 中心點座標Y3
--# Var11 = 中心點座標Z3
--# Var12 = 共用半徑值

function ScriptStart()

  local M1 = Mob.CheckMobPosition(Trigger.Var2,Trigger.Var3,Trigger.Var4,Trigger.Var5,Trigger.Var12)
  local M2 = Mob.CheckMobPosition(Trigger.Var2,Trigger.Var6,Trigger.Var7,Trigger.Var8,Trigger.Var12)
  local M3 = Mob.CheckMobPosition(Trigger.Var2,Trigger.Var9,Trigger.Var10,Trigger.Var11,Trigger.Var12)

  if (M1 == false)and(M2 == false)and(M3 == false) then
    return 0
	
  else
  Scene.PlacementCancel(Trigger.Var1);
  Trigger.PlayFx("MAP_GOAL.fxs");
  Trigger.NextStatus();
    return 1
  end
end