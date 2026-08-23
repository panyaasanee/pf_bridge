--# Var1 = 玩家被強制施家的BuffID
--# Var2 = Buff的標準等級
--# Var3 = 所要檢查的任務ID
--# Var4 = 所要檢查任務的旗標值
--# Var5 = 動態起始Frame
--# Var6 = 動態結束Frame

function ScriptStart()

local Q = Quest.GetQuestFlag(Trigger.Var3);
  if(Q ~= Trigger.Var4)then
    return 0

  else
  Trigger.StartAnimation(Trigger.Var5,Trigger.Var6,1); 
  Player.AddBuff(Trigger.Var1,Trigger.Var2);
  Trigger.NextStatus();
    return 1
  end
end