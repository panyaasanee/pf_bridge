--# Var1 = 瞬移目標點X值
--# Var2 = 瞬移目標點Y值
--# Var3 = 瞬移目標點Z值
--# Var4 = 面向(1~12)
--# Var5 = 所要開啟的配置區ID-1
--# Var6 = 所要開啟的配置區ID-2
--# Var7 = 所要開啟的配置區ID-3
--# Var8 = 所要開啟的配置區ID-4
--# Var9 = 所要開啟的配置區ID-5
--# Var10 = 所要開啟的配置區ID-6
--# Var14 = 傳送、換BGM、開啟最大六個配置區

function ScriptStart()
	Player.Warp(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);
	Player.CameraFocus(Trigger.Var4);
	Scene.ChangeMainMusic("Scn2004");

--# 開啟6個配置區
	Scene.PlacementON(Trigger.Var5);
	Scene.PlacementON(Trigger.Var6);
	Scene.PlacementON(Trigger.Var7);
	Scene.PlacementON(Trigger.Var8);
	Scene.PlacementON(Trigger.Var9);
	Scene.PlacementON(Trigger.Var10);

	return 1

end