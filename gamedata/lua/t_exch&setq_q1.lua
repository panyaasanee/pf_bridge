--# Var1 = 扣除的道具ID
--# Var2 = 扣除的道具數量
--# Var3 = 兌換獲得的道具ID
--# Var4 = 兌換獲得的道具數量
--# Var5 = 所要檢查任務的ID
--# Var6 = 所要檢查任務的旗標值
--# Var7 = 要設定狀態的任務ID
--# Var8 = 任務要設為什麼狀態

function ScriptStart()
  local Q = Quest.GetQuestFlag(Trigger.Var5)
  local I = Player.GetItemNum(Trigger.Var1)
  if(I < Trigger.Var2)then
    Player.ShowMessage(859)
    return 0
  elseif(Q ~= Trigger.Var6)then
    Player.ShowMessage(856) 
    return 0
  else
  Player.RemoveItem(Trigger.Var1,Trigger.Var2);
  Player.AddItem(Trigger.Var3,Trigger.Var4);
  Quest.SetQuestFlag(Trigger.Var7,Trigger.Var8)  
  Trigger.NextStatus();
    return 1
  end
end