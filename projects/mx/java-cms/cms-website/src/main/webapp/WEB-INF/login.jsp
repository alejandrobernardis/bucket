<%@ taglib uri="http://java.sun.com/jsf/html" prefix="h" %>
<%@ taglib uri="http://java.sun.com/jsf/core" prefix="f"%>
<%@ taglib uri="http://richfaces.org/rich" prefix="rich"%>
<%@ taglib uri="http://richfaces.org/a4j" prefix="a4j"%>
<html>
	<head>
		<title></title>
	</head>
	<body>
		<f:view>
			<h:panelGrid columns="2">
				<h:outputText value="Hola" />
				<h:inputText value="" required="true" />
			</h:panelGrid>
			<rich:panel header="Panel" id="pan">
				<h:outputText value="Hola Mundo"  />
				<h:commandButton action="#{mb.search}"></h:commandButton>
			</rich:panel>
		</f:view>
	</body>	
</html>  
