--# Var1 = 所要開啟的場景配置區ID
--# Var2 = 所要回收的場景配置區ID
--# Var3 = 前置機關ID-1
--# Var4 = 前置機關ID-2
--# Var5 = 前置機關ID-3
--# Var6 = 前置機關ID-4
--# Var7 = 前置機關ID-5
--# Var8 = 前置機關ID-6
--# Var9 = 以上6個機關都要為此狀態

function ScriptStart()

  local S1 = Trigger.GetTriggerStatus(Trigger.Var3);
  local S2 = Trigger.GetTriggerStatus(Trigger.Var4);
  local S3 = Trigger.GetTriggerStatus(Trigger.Var5);
  local S4 = Trigger.GetTriggerStatus(Trigger.Var6);
  local S5 = Trigger.GetTriggerStatus(Trigger.Var7);
  local S6 = Trigger.GetTriggerStatus(Trigger.Var8);

  if ((S1 ~= Trigger.Var9)or(S2 ~= Trigger.Var9)or(S3 ~= Trigger.Var9)or(S4 ~= Trigger.Var9)or(S5 ~= Trigger.Var9)or(S6 ~= Trigger.Var9)) then
    return 0 

  else
  Scene.PlacementON(Trigger.Var1);
  Scene.PlacementCancel(Trigger.Var2);
  Trigger.NextStatus();
    return 1
  end
end