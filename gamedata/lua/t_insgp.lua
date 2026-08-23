--# Var1 = 開啟副本選擇介面並顯示指定的副本群組

function ScriptStart()

  Player.LoadInstanceGroup(Trigger.Var1);
  return 1

end