--# Var1 = 玩家藉由機關所要施放的技能
--# Var2 = 技能所指向的座標點X值
--# Var3 = 技能所指向的座標點Y值
--# Var4 = 技能所指向的座標點Z值
--# Var5 = 所要檢查的任務ID-1
--# Var6 = 所要檢查的任務ID-2
--# Var7 = 需要符合任務的旗標值
--# Var8 = 控制角色鏡頭面向哪個方向(1~12)
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()
  local C = Player.GetClass();
  local Q1 = Quest.GetQuestFlag(Trigger.Var5);
  local Q2 = Quest.GetQuestFlag(Trigger.Var6);
  
  if(Q1 ~= Trigger.Var7)and(Q2 ~= Trigger.Var7)then
    return 0 
 
  elseif(C == 1)then --雙刀
  Player.AddAndEquip(2200225,8);
  Player.AddAndEquip(2200225,16);
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Player.CameraFocus(Trigger.Var8)
  Trigger.CastSkillXYZ(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);
  Trigger.NextStatus();  
    return 1

  elseif(C == 2)then --騎士
  Player.AddAndEquip(2200425,8); 
  Player.AddAndEquip(2200625,16);
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Player.CameraFocus(Trigger.Var8)
  Trigger.CastSkillXYZ(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);
  Trigger.NextStatus();
    return 1

  elseif(C == 4)then --槍兵
  Player.AddAndEquip(2201025,8); 
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Player.CameraFocus(Trigger.Var8)
  Trigger.CastSkillXYZ(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);
  Trigger.NextStatus();
    return 1
	
  elseif(C == 8)then --巫毒
  Player.AddAndEquip(2201411,8); 
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Player.CameraFocus(Trigger.Var8)
  Trigger.CastSkillXYZ(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);  
  Trigger.NextStatus();
    return 1	

  elseif(C == 16)then --雷法(浮石)
  Player.AddAndEquip(2200825,8); 
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Player.CameraFocus(Trigger.Var8)
  Trigger.CastSkillXYZ(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);  
  Trigger.NextStatus();
    return 1	

  elseif(C == 32)then --火法(杖)
  Player.AddAndEquip(2201225,8); 
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Player.CameraFocus(Trigger.Var8)
  Trigger.CastSkillXYZ(Trigger.Var1,Trigger.Var2,Trigger.Var3,Trigger.Var4);  
  Trigger.NextStatus();
    return 1

  else 
    return 0	
  end
end