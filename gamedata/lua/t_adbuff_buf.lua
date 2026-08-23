--# Var1 = 身上不能有，啟動後被強制施加的BuffID
--# Var2 = Buff的標準等級

function ScriptStart()

  local B = Player.CheckBuff(Trigger.Var1) 

  if (B == true) then
    return 0

  else
  Player.AddBuff(Trigger.Var1,Trigger.Var2);
  Trigger.NextStatus();
    return 1
  end
end