--# Var1 = 玩家被強制施家的BuffID
--# Var2 = Buff的標準等級
--# Var3 = 所要檢查的任務ID
--# Var4 = 所要檢查任務的旗標值
--# Var5 = 玩家藉由機關所要施放的技能
--# Var6 = 技能所指向的座標點X值
--# Var7 = 技能所指向的座標點Y值
--# Var8 = 技能所指向的座標點Z值

function ScriptStart()

local Q = Quest.GetQuestFlag(Trigger.Var3);
  if(Q ~= Trigger.Var4)then
    return 0

  else
  Trigger.CastSkillXYZ(Trigger.Var5,Trigger.Var6,Trigger.Var7,Trigger.Var8);
  Player.AddBuff(Trigger.Var1,Trigger.Var2);
  Trigger.NextStatus();
    return 1
  end
end