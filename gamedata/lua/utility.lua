--------------------------------------------
--  LuaAdapter 初始化時載入此Script
--  可以在Lua內呼叫這些公用函式
--
--  Roy20110112
--------------------------------------------
math.randomseed(os.time()) --設定亂數種子

-- 計算機率值0~100 (%)是否在 diceValue 之內
function rate(dicevalue)
    
   local r = math.random(0,1000000)/10000;   
   if( r <= dicevalue ) then
      return true;
   else 
      return false;
   end 

end 
