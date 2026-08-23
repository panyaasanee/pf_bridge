--# Var1 = 未使用變數
--# Var2 = 本語法為海神島超級BUFF專用語法

function ScriptStart()

  local C = Player.GetClass();
  local B1 = Player.CheckBuff(8201);
  local B2 = Player.CheckBuff(8202);  
  local B3 = Player.CheckBuff(8203);
  local B4 = Player.CheckBuff(8204);
  local B5 = Player.CheckBuff(8205);
  local B6 = Player.CheckBuff(8206);
  local Q1 = Quest.GetQuestFlag(10);
  local Q2 = Quest.GetQuestFlag(17);
  local Q3 = Quest.GetQuestFlag(708);
  local Q4 = Quest.GetQuestFlag(719);
	if(Quest.GetQuestFlag(1096) ~= 2)then --檢查海魅影死了沒
		if (B1 == true)or(B2 == true)or(B3 == true)or(B4 == true)or(B5 == true)or(B6 == true)or(Q1 == 2)or(Q2 == 2)or(Q3 == 2)or(Q4 == 2) then
			return 0--玩家身上有BUFF就不會重上	
		elseif (C == 1) then--照職業給技能
			Player.AddBuff(8201,100);
			Player.AddBuff(8208,100);
			Player.CastSkillAt(21);
			Trigger.NextStatus();
			return 1;
		elseif (C == 2) then--照職業給技能
			Player.AddBuff(8204,100);
			Player.AddBuff(8208,100);
			Player.CastSkillAt(21);
			Trigger.NextStatus();
			return 1;
		elseif (C == 4) then--照職業給技能
			Player.AddBuff(8202,100);
			Player.AddBuff(8208,100);
			Player.CastSkillAt(21);
			Trigger.NextStatus();
			return 1;  
		elseif (C == 8) then--照職業給技能
			Player.AddBuff(8205,100);
			Player.AddBuff(8208,100);
			Player.CastSkillAt(21);
			Trigger.NextStatus();
			return 1;	
		elseif (C == 16) then--照職業給技能
			Player.AddBuff(8203,100);
			Player.AddBuff(8208,100);
			Player.CastSkillAt(21);
			Trigger.NextStatus();
			return 1;  
		elseif (C == 32) then--照職業給技能
			Player.AddBuff(8206,100);
			Player.AddBuff(8208,100);
			Player.CastSkillAt(21);  
			Trigger.NextStatus();
			return 1;
		else 
			return 0;	
		end
	else 
		return 0;				
	end		
end