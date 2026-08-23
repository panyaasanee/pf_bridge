--# Var1 = 玩家被強制施家的BuffID
--# Var2 = Buff的標準等級
--# Var3 = 所要檢查的任務ID
--# Var4 = 所要檢查任務的旗標值
--# Var9 = 2014-4-17開發版未使用-使用前需再check

function ScriptStart()

local Q = Quest.GetQuestFlag(Trigger.Var3);
  if(Q ~= Trigger.Var4)then
    return 0

  else
  Player.AddBuff(Trigger.Var1,Trigger.Var2);
  Trigger.NextStatus();
    return 1
  end
end