--# Var1 = 玩家被強制施家的BuffID
--# Var2 = Buff的標準等級

function ScriptStart()
  
  Player.AddBuff(Trigger.Var1,Trigger.Var2);

  return 1
end