--# Var1 = 扣除的道具ID
--# Var2 = 扣除的道具數量
--# Var3 = 兌換獲得的道具ID
--# Var4 = 兌換獲得的道具數量
--# Var5 = 所要檢查機關的ID
--# Var6 = 所要檢查機關的狀態
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var1);
  local S = Trigger.GetTriggerStatus(Trigger.Var5);

  if(I < Trigger.Var2)then
    return 0
  elseif(S ~= Trigger.Var6)then
    return 0

  else
  Player.RemoveItem(Trigger.Var1,Trigger.Var2);
  Player.AddItem(Trigger.Var3,Trigger.Var4);
  Trigger.NextStatus();
    return 1
  end
end