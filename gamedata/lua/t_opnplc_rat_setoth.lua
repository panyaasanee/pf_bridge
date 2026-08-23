--# Var1 = 成功開啟的機率
--# Var2 = 觸發失敗時要指定本機關的狀態為(var2)
--# Var3 = 所要開啟的場景配置區ID
--# Var4 = 觸發失敗時同時要被指定狀態的機關ID
--# Var5 = 觸發失敗時同時指定其他機關的狀態為(var5)
--# Var6 = 觸發成功要顯示的系統訊息(var6)
function ScriptStart()

  if(not rate(Trigger.Var1))then
  Trigger.SetStatus(Trigger.Var2);
  Trigger.SetTriggerStatus(Trigger.Var4,Trigger.Var5);
    return 1
  
  else
  Scene.PlacementON(Trigger.Var3);
  Party.ShowMessage(Trigger.Var6)
  Trigger.NextStatus();
    return 1
  end
end