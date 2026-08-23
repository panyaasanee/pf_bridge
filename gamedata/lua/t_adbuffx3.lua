--# Var1 = 產砆眏琁產BuffID-1
--# Var2 = Buff夹非单-1
--# Var3 = 產砆眏琁產BuffID-2
--# Var4 = Buff夹非单-2
--# Var5 = 產砆眏琁產BuffID-3
--# Var6 = Buff夹非单-3

function ScriptStart()
  
  Player.AddBuff(Trigger.Var1,Trigger.Var2);
  Player.AddBuff(Trigger.Var3,Trigger.Var4);
  Player.AddBuff(Trigger.Var5,Trigger.Var6);
  Trigger.NextStatus();
  return 1
end