--# Var1 = 晃動鏡頭的震矩
--# Var2 = 晃動鏡頭所持續的時間
--# Var3 = 所要控制的機關ID
--# Var4 = 檢查所要控制機關的狀態是否符合
--# Var5 = 動態起始Frame
--# Var6 = 動態結束Frame
--# Var7 = 受控制機關的作用後狀態
--# Var8 = 所要檢查的其他機關ID
--# Var9 = 所要檢查其他機關的狀態
--# Var10 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local S1 = Trigger.GetTriggerStatus(Trigger.Var3);
  local S2 = Trigger.GetTriggerStatus(Trigger.Var8);
  
  if((S1 ~= Trigger.Var4)or(S2 ~= Trigger.Var9))then
    return 0  
  else
  Scene.CamaraShake(Trigger.Var1,Trigger.Var2); 
  Trigger.StartTriggerAnimation(Trigger.Var3,Trigger.Var5,Trigger.Var6,2); 
  Trigger.SetTriggerStatus(Trigger.Var3,Trigger.Var7);
  Trigger.NextStatus();
    return 1
  end;
end