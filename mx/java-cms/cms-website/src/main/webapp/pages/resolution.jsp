
<%@page import="org.apache.commons.lang.StringUtils"%><html>
	<head>
		<%
			String lang = request.getParameter("lang");
			String content = request.getParameter("content");
			String queryString = "";
			if( StringUtils.isNotEmpty(lang) ){
				queryString += "&lang=" + lang; 
			}
			if( StringUtils.isNotEmpty(content) ){
				queryString += "&content=" + content; 
			}
		
		%>
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
		<SCRIPT language="JavaScript">
		<!--
			var width = screen.width;
			var height = screen.height;  
			var redirectPage = '<%=request.getContextPath()+"/pages/axo.jsf"%>' + "?width=" +width+"&height="+height+'<%=queryString%>'; 
 			window.location=redirectPage;
		//-->
		</SCRIPT>

	</head> 	
	<body>
		 <table align="center"><tr><td class="blankspace">
	    </td></tr>
	    <tr><td>
	    	<img src="<%= request.getContextPath() %>/web-resources/img/logoInicio.png?dummy=<%= Math.round( Math.random() * 1000000 ) %>">
	    </td></tr></table>
	</body>
</html>