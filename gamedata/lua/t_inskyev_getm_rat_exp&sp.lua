--# Var1 = 觸發機關所獲得的關鍵事件次數
--# Var2 = 獲得額外經驗值與技能點獎勵的機率
--# Var3 = 給予道具的ID
--# Var4 = 給予道具的數量
--# Var5 = 此數值*觸發者等級值=實際獲得經驗值與技能點
--# Var9 = 2014-4-17開發版未使用-使用前需再check
function ScriptStart()

  if(not rate(Trigger.Var2))then 
  Instance.AddKeyEvent(Trigger.Var1);
  Player.AddItem(Trigger.Var3,Trigger.Var4);
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1

  else
  Instance.AddKeyEvent(Trigger.Var1);
  Player.AddItem(Trigger.Var3,Trigger.Var4);
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Player.AddExp(Player.GetLv()*Trigger.Var5);
  Player.AddSkillPoint(Player.GetLv()*Trigger.Var5);
  Trigger.NextStatus();
    return 1
  end
end