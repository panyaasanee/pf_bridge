--# Var1 = 等級限制，低於此等級不會觸發
--# Var2 = 成功開啟的機率
--# Var3 = 觸發成功時所要開啟的場景配置區ID


function ScriptStart()

  local L = Player.GetLv();
  if(L < Trigger.Var1)then
    return 0 

  elseif(not rate(Trigger.Var2))then
  Trigger.NextStatus();
    return 1
  
  else
  Scene.PlacementON(Trigger.Var3);
  Trigger.NextStatus();
    return 1
  end
end