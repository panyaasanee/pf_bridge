--# Var1 = 所要檢查的圖鑑ID
--# Var2 = 操作者限制等級
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local L = Player.GetLv();
  local C = Player.CheckCollect(Trigger.Var1);
  if((L < Trigger.Var2) or (C ~= true))then
    return 0
  
  else
  Trigger.NextStatus()
    return 1
  end
end