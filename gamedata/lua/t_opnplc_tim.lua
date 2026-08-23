--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 副本時間-當前剩餘(VarX)=副本開始多久之後
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local T = Instance.GetLastingTime();
  if (T > Trigger.Var2)then
    return 0
  else
  Scene.PlacementON(Trigger.Var1);
  Trigger.NextStatus();
  return 1
end


end