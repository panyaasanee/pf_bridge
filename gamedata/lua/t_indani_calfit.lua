--# Var1 = 要受控制機關的ID
--# Var2 = 受控制機關的初始狀態
--# Var3 = 機關動態起始Frame
--# Var4 = 機關動態結束Frame
--# Var5 = 受控制機關的作用後狀態
--# Var6 = 要呼叫進入戰鬥的怪物配置區ID
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local S = Trigger.GetTriggerStatus(Trigger.Var1);
  if(S ~= Trigger.Var2)then
    return 0
  
  else
  Trigger.StartTriggerAnimation(Trigger.Var1,Trigger.Var3,Trigger.Var4,1); 
  Trigger.SetTriggerStatus(Trigger.Var1,Trigger.Var5);
 -- Scene.CallPlacementFight(Trigger.Var6)
  Trigger.NextStatus()
    return 1
  end
end