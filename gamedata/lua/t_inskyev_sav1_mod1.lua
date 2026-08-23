--# Var1 = 觸發機關所獲得的關鍵事件次數
--# Var2 = 不能死的怪物配置區ID
--# Var3 = 必須要殺死的怪物配置區ID
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local M1 = Scene.CheckPlacementAlive(Trigger.Var2);
  local M2 = Scene.CheckPlacementAlive(Trigger.Var3);
  if((M1 == false)or(M2 == true))then
    return 0

  else
  Instance.AddKeyEvent(Trigger.Var1)
  Trigger.NextStatus();
    return 1
  end
end