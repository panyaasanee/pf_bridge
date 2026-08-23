--# Var1 = 等級限制，低於此等級不會觸發
--# Var2 = 成功開啟的機率
--# Var3 = 觸發成功時所要開啟的場景配置區ID
--# Var4 = 所要檢查&要上的BUFF ID
--# Var5 = BUFF標準等級
--# Var6 = 用於各海域海盜船機關


function ScriptStart()  
  
	if(Player.CheckBuff(Trigger.Var4)) then --檢查玩家身上有VAR4的BUFF ID的話
		
		return 0 --不觸發航海事件
	else --所以沒有VAR4的BUFF 就會進入航海事件是否要被觸發的流程

		if(Player.GetLv() > Trigger.Var1)then --玩家等級大於可觸發事件等級的話
  
			if (rate(Trigger.Var2)) then --擲骰有通過的話
			
				Scene.PlacementON(Trigger.Var3);
				Player.AddBuff(Trigger.Var4,Trigger.Var5);  
			end
			--Trigger.NextStatus();
			return 1
		else
		
			return 0
		end	
	end
end