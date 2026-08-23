--# Var1 = 檢查有無開過的機關-1
--# Var2 = 檢查有無開過的機關-2
--# Var3 = 檢查有無開過的機關-3
--# Var4 = 鑰匙道具ID
--# Var5 = 寶箱內給予物品ID
--# Var6 = 機率檢查沒過時執行的掉落群

function ScriptStart()
  local T1 = Trigger.GetTriggerStatus(Trigger.Var1);
  local T2 = Trigger.GetTriggerStatus(Trigger.Var2);
  local T3 = Trigger.GetTriggerStatus(Trigger.Var3);
  local I1 = Player.GetItemNum(Trigger.Var4);
  local I2 = Player.GetItemNum(Trigger.Var5);    

  if I1 == 0 then
    Player.ShowMessage(859)
    return 0
  
  elseif(T1+T2+T3 == 3)and(I2 == 0)then
  Player.AddItem(Trigger.Var5,1);
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1

  elseif(T1+T2+T3 == 0)and(rate(25)and(I2 == 0))then
  Player.AddItem(Trigger.Var5,1);
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1  

  elseif(T1+T2+T3 == 1)and(rate(50)and(I2 == 0))then
  Player.AddItem(Trigger.Var5,1);
  Trigger.HideModel();
  Trigger.NextStatus();
    return 1    

  elseif(T1+T2+T3 == 2)and(rate(75)and(I2 == 0))then
  Player.AddItem(Trigger.Var5,1);
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1    
	
  else
  Player.DropProcess(Trigger.Var6);
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
  end
end