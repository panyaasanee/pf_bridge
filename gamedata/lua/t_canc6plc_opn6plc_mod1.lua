--# Var1 = 所要關閉的配置區ID-1
--# Var2 = 所要關閉的配置區ID-2
--# Var3 = 所要關閉的配置區ID-3
--# Var4 = 所要關閉的配置區ID-4
--# Var5 = 所要關閉的配置區ID-5
--# Var6 = 所要關閉的配置區ID-6
--# Var7 = 所要開啟的配置區ID-1
--# Var8 = 所要開啟的配置區ID-2
--# Var9 = 所要開啟的配置區ID-3
--# Var10 = 所要開啟的配置區ID-4
--# Var11 = 所要開啟的配置區ID-5
--# Var12 = 所要開啟的配置區ID-6
--# Var13 = 所要檢查的配置區，若為0則直接通過
--# Var14 = 檢查配置區的怪物是否活著。回收最大六個配置區，並同時開啟最大六個配置區

function ScriptStart()
--# 欲檢查的配置區若為0，則直接執行關閉與開啟配置區
	if(Trigger.Var13 == 0)then
		Scene.PlacementCancel(Trigger.Var1);
		Scene.PlacementCancel(Trigger.Var2);
		Scene.PlacementCancel(Trigger.Var3);
		Scene.PlacementCancel(Trigger.Var4);
		Scene.PlacementCancel(Trigger.Var5);
		Scene.PlacementCancel(Trigger.Var6);
		Scene.PlacementON(Trigger.Var7);
		Scene.PlacementON(Trigger.Var8);
		Scene.PlacementON(Trigger.Var9);
		Scene.PlacementON(Trigger.Var10);
		Scene.PlacementON(Trigger.Var11);
		Scene.PlacementON(Trigger.Var12);
		Trigger.NextStatus();
		return 1
	else
 --# 欲檢查的配置區不為0，則檢查該配置區的怪物是否活著
   local M = Scene.CheckPlacementAlive(Trigger.Var13); 
		if(M == true)then
		return 0
		
		else
			Scene.PlacementCancel(Trigger.Var1);
			Scene.PlacementCancel(Trigger.Var2);
			Scene.PlacementCancel(Trigger.Var3);
			Scene.PlacementCancel(Trigger.Var4);
			Scene.PlacementCancel(Trigger.Var5);
			Scene.PlacementCancel(Trigger.Var6);
		  	Scene.PlacementON(Trigger.Var7);
			Scene.PlacementON(Trigger.Var8);
			Scene.PlacementON(Trigger.Var9);
			Scene.PlacementON(Trigger.Var10);
			Scene.PlacementON(Trigger.Var11);
			Scene.PlacementON(Trigger.Var12);
			Trigger.NextStatus();
			return 1
		end

	return 0
	end
end