--# Var1 = 所要呼叫的怪物群組
--# Var2 = 所呼叫怪物隊伍的位置(MarkerID)
--# Var3 = 所要檢查並扣除道具的ID
--# Var4 = 所要檢查並扣除道具的數量

function ScriptStart()
  if(Player.GetItemNum(Trigger.Var3) < Trigger.Var4)then
	if(Trigger.GetContactMode(22) == 1)then
		Player.ShowMessage(859)
	end
    return 0 
  else
	Player.RemoveItem(Trigger.Var3,Trigger.Var4);
	Mob.CallMob(Trigger.Var1,Trigger.Var2);
	Trigger.NextStatus();  
    return 1
  end
end