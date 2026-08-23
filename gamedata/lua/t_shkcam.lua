--# Var1 = 晃動鏡頭的震矩
--# Var2 = 晃動鏡頭所持續的時間
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  Scene.CamaraShake(Trigger.Var1,Trigger.Var2); 
  Trigger.NextStatus();
  return 1

end