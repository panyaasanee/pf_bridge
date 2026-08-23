--# Var1 = 所要檢查的圖鑑ID
--# Var2 = 指定的副本ID內才啟用

function ScriptStart()
  local I = Instance.GetInstanceID();
  local C = Player.CheckCollect(Trigger.Var1);
  if((I ~= Trigger.Var2) or (C ~= true))then
    Player.ShowMessage(860)  
    return 0
  
  else
  Trigger.NextStatus()
    return 1
  end
end