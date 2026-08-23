--# Var1 = 成功開啟的機率
--# Var2 = 要受控制機關的ID
--# Var3 = 受控制機關的初始狀態
--# Var4 = 本機關觸發失敗時要切換到什麼狀態
--# Var5 = 受控制機關觸發成功時要切換到什麼狀態
--# Var6 = 受控制機關觸發失敗時要切換到什麼狀態
--# Var7 = 動態起始時間
--# Var8 = 動態結束時間
--# Var9 = 觸發者隊伍全員要被放的技能
--# Var10 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local S = Trigger.GetTriggerStatus(Trigger.Var2);
  if(not rate(Trigger.Var1)or(S ~= Trigger.Var3))then
  Trigger.SetStatus(Trigger.Var4);
  Trigger.SetTriggerStatus(Trigger.Var2,Trigger.Var6);
    return 1

  else
  Trigger.SetTriggerStatus(Trigger.Var2,Trigger.Var5);
  Trigger.StartTriggerAnimation(Trigger.Var4,Trigger.Var7,Trigger.Var8,2); 
  Party.CastSkillAt(Trigger.Var9);
  Trigger.NextStatus();
    return 1
  end;
end