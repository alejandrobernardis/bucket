/*
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 19/08/2013 11:07
*/

package {
   public class IronMan {
       private static const CHARS:Array=new Array(48,49,50,51,52,53,54,55,56,57,65,66,67,68,69,70);
       private static const SEPARATOR:uint=45;
       private static const MIN_LISTED_VALUE:Number=0;
       private static const MAX_LISTED_VALUE:Number=64;
       
       private static const KEYS:Array = new Array(
           '6P2w4h', '55I7Jy', 'h445zT', 'k8P7K2', '89F4zU', '8FZ18v', 
           'T9jc93', 'C2e6Y8', '33eCj3', 'P666CU', 'k76K7z', 'b1P91z', 
           'T487Dy', 'e144rw', 'R463Ol', 'JD2i46', 'q99S5k', '707EyK', 
           'XdA593', 'C38B2m', '4en56s', 'sF294b', '42CJ8Z', '615wGX', 
           '3cMP49', 'Wrt658', '9BI7z2', 'x2pk11', '5naP05', 'j7V6m6', 
           '7LGP31', '98fZ9o', 'bww606', '4Li48o', 'f4Jl42', '2E28yA', 
           '98ad9P', '1da71h', '3i39Tm', '8C29oM', '6Hk8S4', 'W8m58t', 
           '29sqQ8', '91h7hp', 'M265Fh', '836teu', '7y5K2Y', '363uHb', 
           '8o4fz2', '19KU0q', 'f2z8t0', '85S7Bw', 'G6oY22', 'yWU415', 
           '11E9cW', '1R9pJ2', 'zH78B7', '9OA11E', 'K9V07X', '96wh2J', 
           '998tro', 'L2O45Z', 'g79Ok0', '83s4rb', '52cm8X', 'O4U8w2', 
           'B8Is05', '3R7fS8', 'Z3F4H1', 'qN2f21', '8ZUp80', 'V8gB92', 
           'a1I41T', 'Qk192E', '5wt5r6', '38wSl2', 'w28x2m', '7Z3eT4', 
           'a5Le92', '343ily', '79Nt9v', '11ThX3', 'gI8s33', '22Q4DQ', 
           'iF43g3', '70Z6Zz', '5G5zx6', '9g0N3c', 'o30yf1', 's6qD90', 
           '7r2L9y', 'M2a9k0', '53B5Lf', 'YEr771', '1Cg61K', '8moG98', 
           '60LF4o', '5J5Le9', '8S8rj7', '24Ll4H'
       );
       
       public static function listed(min:Number=NaN, max:Number=NaN):Array {
           var vmin:Number=Math.min(min,max)||MIN_LISTED_VALUE;
           var vmax:Number=(!isNaN(min))?Math.max(min,max):max||MAX_LISTED_VALUE;
           var list:Array=new Array();
           while(vmin<=vmax){
               list.push(vmin++);
           } return list;
       }

       public static function uniqueRandom(min:Number=NaN, max:Number=NaN):Array {
           var list:Array=new Array();
           var positions:Array=listed(min,max);
           var vLength:Number=positions.length;
           var vPosition:Number;
           for(var a:uint=0; a<vLength; a++){
               vPosition=Math.floor(Math.random()*(vLength-a));
               list.push(positions[vPosition]);
               positions.splice(vPosition,1);
           } return list;
       }

       public static function hash():String {
           var d:Date=new Date();
           var dm:String=new String(d.getMonth()+1);
           var dd:String=d.getDate().toString();
           var _date:String=new Array(
               d.getFullYear().toString(),
               (dm.length>1)?dm:'0'+dm,
               (dd.length>1)?dd:'0'+dd
           ).join('/');
           var dh:String=d.getHours().toString();
           var dmm:String=d.getMinutes().toString();
           var ds:String=d.getSeconds().toString();
           var _time:String=new Array(
               (dh.length>1)?dh:'0'+dh,
               (dmm.length>1)?dmm:'0'+dmm,
               (ds.length>1)?ds:'0'+ds
           ).join(':');
           _time+='.'+d.getMilliseconds().toString();
           var _domain:String='casino8.com';
           var _key:String=KEYS[uniqueRandom(0, KEYS.length-1)[0]];
           var _literal:String='^'+new Array(_date, _time, _domain, _key).join('|')+'$';
           var _uid:String=IronMan.uid();
           var _hash:String=IronMan.doit(_literal, _uid);
           return 'I'+_hash+'|'+_uid;
       }

       public static function uid(template:Array=null):String {
           if(!template){template=new Array(8,4,4,4,12);}
           var uid:Array=new Array();
           var last:int=template.length-1;
           for(var a:uint=0; a<template.length; a++){
               for(var b:uint=0; b<template[a]; b++){uid.push(CHARS[Math.floor(Math.random()*CHARS.length)]);}
               if(a<last){uid.push(SEPARATOR);}
           } var time:String=String("0000000"+new Date().getTime().toString(16).toUpperCase()).substr(Math.random()*template[last]);
           return String(String.fromCharCode.apply(null,uid)).substr(0,-time.length)+time;
       }

       public static function doit(g:String, h:String):String {
           var a:String="";
           var b:int=0;
           for(var i:int=0;i<g.length;++i){
               var c:int=g.charCodeAt(i)^h.charCodeAt(b);
               var d:String=c.toString();
               if(c<10){d="00"+d;}else if(c<100){d="0"+d;}
               a=a+d;
               if(b==h.length-1){b=0;}else{b++;}
           } return a;
       }

   }
}
