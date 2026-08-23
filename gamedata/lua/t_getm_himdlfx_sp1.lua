function ScriptStart()
  if( Player.SuveryOwner() == false ) then	
	Player.ShowMessage(882)	
	return 0
  end

  Player.AddItem(2600002,1)
  Trigger.HideModel();
  Trigger.PlayFx("BgFx0005_002.fxs");
  Trigger.NextStatus();
    return 1
end
