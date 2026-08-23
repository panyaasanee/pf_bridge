--# Var1 = 移除觸發者身上BuffID
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Player.RemoveBuff(Trigger.Var1);
  Trigger.NextStatus();
  return 1
end