--# Var1 = 所要檢查的圖鑑ID
--# Var2 = 要檢查是否存活的怪物ID
--# Var3 = 所要執行的掉落群
--# Var4 = 機關物件起始動態秒數
--# Var5 = 機關物件結束動態秒數
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  local C = Player.CheckCollect(Trigger.Var1);
  local M = Mob.CheckMobalive(Trigger.Var2);
  
  if(C ~= true)then
    return 0  

  elseif(M ~= true)then
  Trigger.StartAnimation(Trigger.Var4,Trigger.Var5,1,1); 
  Trigger.NextStatus();

  else
  Player.DropProcess(Trigger.Var3); 
  Trigger.StartAnimation(Trigger.Var4,Trigger.Var5,1,1); 
  Trigger.NextStatus();
    return 1
  end;
end
