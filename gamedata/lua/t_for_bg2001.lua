--# Var1 = 0星墜落太陽專用

function ScriptStart()
  local I1 = Instance.GetInstanceID();
  
  if(I1 == 1028)then
	Trigger.SetTriggerStatus(2,2)
	Trigger.SetTriggerStatus(23,2)
	Trigger.SetTriggerStatus(53,2)
	Trigger.SetTriggerStatus(27,2)
	Trigger.SetTriggerStatus(10,2)
	Trigger.SetTriggerStatus(30,2)
	Trigger.SetTriggerStatus(16,2)
	Trigger.SetTriggerStatus(20,2)
	Trigger.SetTriggerStatus(22,2)
	Trigger.SetTriggerStatus(18,2)
	Trigger.HideTriggerModel(91)  
	Trigger.HideTriggerModel(38)  
	Trigger.HideTriggerModel(42)  
	Trigger.HideTriggerModel(40)  
	Trigger.HideTriggerModel(39)  
	Trigger.HideTriggerModel(41)  
	Trigger.HideTriggerModel(93)  
  	Trigger.HideTriggerModel(37)   
    return 1 
	
  else
  	Scene.PlacementCancel(9) 
    return 0
  end
end