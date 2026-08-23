--# Var1 = 給予玩家道具的ID
--# Var2 = 道具最多持有數量
--# Var3 = 所要檢查任務的ID
--# Var4 = 所要檢查任務的旗標值
--# Var5 = 取得道具的機率
--# Var6 = 若取得道具失敗，會觸發的技能

function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var1);
  local Q = Quest.GetQuestFlag(Trigger.Var3)

  if(I >= Trigger.Var2)then
    Player.ShowMessage(855)
    return 0
	
  elseif(Q ~= Trigger.Var4)then
	Player.ShowMessage(856)
    return 0
	
  elseif rate(Trigger.Var5) then
  Player.AddItem(Trigger.Var1,1);
  Trigger.HideModel();
  Trigger.NextStatus();
    return 1

  else
  Player.CastSkillAt(Trigger.Var6);
  Trigger.HideModel();
  Trigger.NextStatus();
    return 1
  end
end