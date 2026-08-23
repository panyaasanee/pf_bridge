--# Var1 = 給予玩家道具的ID
--# Var2 = 道具最多持有數量
--# Var3 = 所要檢查機關的ID
--# Var4 = 所要檢查機關的狀態
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local I = Player.GetItemNum(Trigger.Var1);
  local S = Trigger.GetTeiggerStatus(Trigger.Var3);

  if(I >= Trigger.Var2)then
    return 0
  elseif(S ~= Trigger.Var4)then
    return 0

  else
  Player.AddItem(Trigger.Var1,1)
  Trigger.NextStatus();
    return 1
  end
end