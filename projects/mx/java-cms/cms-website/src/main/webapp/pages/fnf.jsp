<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
  <head>
    <title>Error</title>
    <style type="text/css">
    	body{
    		background-image: url("<%= request.getContextPath() %>/web-resources/img/bg_inicio.jpg");
    	}
    	.blankspace{
    		height: 100px;
    	}
    	.message{
    		color: #000000;
    		font-family: arial, sans-serif;
    		font-size: 12px;
    		text-align: center;
    		border:1px solid #FFFFFF;
    		padding: 20px;
    		background-color: #FFFFFF;
    	}
    	.message2{
    		color: #FFFFFF;
    		font-family: arial, sans-serif;
    		font-size: 12px;
    		text-align: center;
    		border:1px solid #FFFFFF;
    		padding: 20px;
    	}
    	
    	a{
    		color:#FFFFFF;
    		font-weight: bold;
    		font-size: 15px;
    		font-style: italic;
    	}
    </style>
  </head>
  
  <body >
    <table align="center"><tr><td class="blankspace">
    </td></tr>
    <tr><td>
    
    	<img src="<%= request.getContextPath() %>/web-resources/img/logoInicio.png?dummy=<%= Math.round( Math.random() * 1000000 ) %>">
    </td></tr></table>
    <table align="center"><tr><td class="message2">
    	No se ha encontrado la página que busca<br/><br/>
    	Page not Found<br/><br/>
    	<a href="<%= request.getContextPath()%>/pages/axo.jsf">Home</a>
    	 
    </td></tr>
    
    </table>
    
    
    
  </body>
</html>
