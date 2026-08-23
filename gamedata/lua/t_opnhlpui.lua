--# Var1 = 要開啟的說明文字ID
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  
  Player.OpenHelpUI(Trigger.Var1)
  Trigger.NextStatus();
    return 1
end