--# Var1 = 所要關閉的配置區ID-1
--# Var2 = 所要關閉的配置區ID-2
--# Var3 = 所要檢查的機關ID
--# Var4 = 所要檢查機關的狀態值
--# Var5 = 副本時間-當前剩餘(VarX)=副本開始多久之後
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local TM = Instance.GetLastingTime();
  local T = Trigger.GetTriggerStatus(Trigger.Var3);

  if ((TM > Trigger.Var5)or(T ~= Trigger.Var4))then
    return 0

  else
  Scene.PlacementOFF(Trigger.Var1);
  Scene.PlacementOFF(Trigger.Var2);  
  Trigger.NextStatus();
    return 1
  end
end