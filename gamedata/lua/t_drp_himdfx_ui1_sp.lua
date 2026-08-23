--# Var1 = 副本入口1所要執行的掉落群
--# Var2 = 副本入口1的編號 
--# Var3 = 副本入口2所要執行的掉落群
--# Var4 = 副本入口2的編號
--# Var5 = 本語法為登島特殊寶箱專用 
function ScriptStart()
  local I = Player.GetItemNum(2600081);
  local I1 = Instance.GetInstanceID();
  
  if(I > 0 and I1 == Trigger.Var2)then
	Player.DropProcess(Trigger.Var1);
	Player.RemoveItem(2600081,1); 
	Trigger.HideModel();
	Trigger.PlayFx("BgFx0005_002.fxs");  
	Trigger.NextStatus();
    return 1
	
  else if(I > 0 and I1 == Trigger.Var4)then	
	Player.DropProcess(Trigger.Var3);
	Player.RemoveItem(2600081,1); 
	Trigger.HideModel();
	Trigger.PlayFx("BgFx0005_002.fxs");  
	Trigger.NextStatus();	
   return 1	
   
  else
    Player.ShowMessage(859)
    return 0  
	end
  end
end