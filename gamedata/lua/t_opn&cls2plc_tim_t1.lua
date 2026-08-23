--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 副本時間-當前剩餘(VarX)=副本開始多久之後
--# Var3 = 前置機關ID
--# Var4 = 前置機關應有狀態值
--# Var5 = 同時要關閉的另一個配置區ID-1
--# Var6 = 同時要關閉的另一個配置區ID-2
--# Var9 = 2014-4-17開發版未使用-使用前需再check

function ScriptStart()

  local TM = Instance.GetLastingTime();
  local T = Trigger.GetTriggerStatus(Trigger.Var3);

  if ((TM > Trigger.Var2)or(T ~= Trigger.Var4))then
    return 0

  else
  Scene.PlacementON(Trigger.Var1);
  Scene.PlacementOFF(Trigger.Var5);
  Scene.PlacementOFF(Trigger.Var6);
  Trigger.NextStatus();
    return 1
  end
end