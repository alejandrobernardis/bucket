package activia.simon.shooter.core {
	import pq.core.CoreStatic;
	
	
	public class FacebookXMLHelper extends CoreStatic {
		
		public function FacebookXMLHelper() {
			
		}
		
		public static const XML_CONFIG:XML = <recordset>	
	<config>		
		<info>
			<client><![CDATA[Elea]]></client>
			<brand><![CDATA[Aziatop]]></brand>
			<project><![CDATA[Declará la paz en tu estómago.]]></project>
			<url><![CDATA[http://www.project.com]]></url>
			<email><![CDATA[info@project.com]]></email>
		</info>
		<allowDomain>
			<domain><![CDATA[*]]></domain>
			<domain><![CDATA[apps.facebook.com]]></domain>
			<domain><![CDATA[apps.*.facebook.com]]></domain>
			<domain><![CDATA[*.publiquest.net]]></domain>
		</allowDomain>
		<paths>
			<base><![CDATA[http://staging.publiquest.net/elea/aziatop/fb/]]></base>
			<swf><![CDATA[swf]]></swf>
			<xml><![CDATA[xml]]></xml>
			<img><![CDATA[img]]></img>
			<snd><![CDATA[snd]]></snd>
			<php><![CDATA[includes]]></php>
		</paths>
		<game><![CDATA[{config.paths.xml}/game.xml]]></game>
		<debug>
			<level><![CDATA[all]]></level>
			<appender><![CDATA[output]]></appender>
			<filter><![CDATA[*]]></filter>
			<separator><![CDATA[|]]></separator>
		</debug>
	</config>
</recordset>;
		
		public static const XML_GAME:XML = <recordset>	
	<config>
		<time><![CDATA[360000]]></time>
		<delay><![CDATA[50]]></delay>
		<countdown><![CDATA[3]]></countdown>
		<canvas>
			<axis><![CDATA[8 40]]></axis>
			<size><![CDATA[621 380]]></size>
		</canvas> 		
		<localization><![CDATA[{config.paths.xml}/localization.xml]]></localization>
	</config>
	<serverSide>
		<scoreregiste>
			<param id="score_name"><![CDATA[name]]></param>
			<param id="score_value"><![CDATA[score]]></param>
			<url><![CDATA[{config.paths.php}/score.php]]></url>
		</scoreregiste>
		<ranking>
			<pattern><![CDATA[<record id="{1}" score="{2}">{3}</record>]]></pattern>
			<url><![CDATA[{config.paths.php}/ranking_xml.php]]></url>
		</ranking>
	</serverSide>	
	<socialNetworks>
		<twitter target="_blank">
			<message><![CDATA[@twitter@Jugué con #aziatop y declaré la paz en mi estómago. ¿Quién se atreve a superar las @score@ bombas desactivadas? www.pazentuestomago.com]]></message>			
			<replace id="@score@"><![CDATA[score_value]]></replace>
			<replace id="@twitter@"><![CDATA[http://twitter.com/home?status=]]></replace>
		</twitter>
		<facebook target="_blank">			
			<message><![CDATA[{config.paths.php}/facebook.php?name=@name@&score=@score@]]></message>
			<replace id="@name@"><![CDATA[score_name]]></replace>
			<replace id="@score@"><![CDATA[score_value]]></replace>
		</facebook>
	</socialNetworks>	
	<facebook>
		<share>
			<![CDATA[http://apps.facebook.com/testaziatop/invite.php]]>
		</share>
		<wall>
			<method><![CDATA[resultado]]></method>
			<param id="score_value"><![CDATA[score]]></param>
		</wall>
	</facebook>
	<screens>
		<screen id="home" controller="activia.simon.shooter.ui.screens::GHome"/>
		<screen id="instructions" controller="activia.simon.shooter.ui.screens::GInstructions"/>
		<screen id="game" controller="activia.simon.shooter.ui.screens::GContainer"/>
		<screen id="gameover" controller="activia.simon.shooter.ui.screens::GOver"/>
		<screen id="gameexit" controller="activia.simon.shooter.ui.screens::GExit"/>
		<screen id="scoreregiste" controller="activia.simon.shooter.ui.screens::GScoreRegiste"/>
		<screen id="ranking" controller="activia.simon.shooter.ui.screens::GRanking"/>
	</screens>	
	<tween>
		<speedx><![CDATA[2]]></speedx>
		<speedy><![CDATA[.2]]></speedy>
		<desacx><![CDATA[33.3333]]></desacx>
		<desacy><![CDATA[.8]]></desacy>
		<angle><![CDATA[270]]></angle>
		<range><![CDATA[20]]></range>
		<delta><![CDATA[100]]></delta>
		<duration><![CDATA[66]]></duration>
	</tween>	
	<sounds>
		<sound id="fxDefault"><![CDATA[fxDefault]]></sound>
		<sound id="fxAlliesBomb"><![CDATA[fxAlliesBomb]]></sound>
		<sound id="fxProtonsBomb"><![CDATA[fxProtonsBomb]]></sound>
		<sound id="fxThreastsBomb"><![CDATA[fxThreastsBomb]]></sound>
	</sounds>	
	<actors>
		<area><![CDATA[621 380]]></area>
		<origin><![CDATA[left]]></origin>
		<framerate><![CDATA[60]]></framerate>
		<critical><![CDATA[40]]></critical>
		<delay>
			<level id="1"><![CDATA[4000]]></level>
			<level id="2"><![CDATA[3000]]></level>
			<level id="3"><![CDATA[2000]]></level>
		</delay>
		<assets max="16" min="4">
			<asset id="acid" controller="activia.simon.shooter.ui.actors::Acid">
				<scmin><![CDATA[.2]]></scmin>
				<scmax><![CDATA[.5]]></scmax>
				<spmin><![CDATA[1]]></spmin>
				<spmax><![CDATA[5]]></spmax>
				<value><![CDATA[]]></value>
				<coef><![CDATA[10]]></coef>
				<sound><![CDATA[]]></sound>
			</asset>
			<asset id="allies" controller="activia.simon.shooter.ui.actors::AlliesBomb">
				<scmin><![CDATA[.5]]></scmin>
				<scmax><![CDATA[.8]]></scmax>
				<spmin><![CDATA[4]]></spmin>
				<spmax><![CDATA[5]]></spmax>
				<value><![CDATA[*]]></value>
				<coef><![CDATA[25]]></coef>
				<sound><![CDATA[fxAlliesBomb]]></sound>
			</asset>
			<asset id="protons" controller="activia.simon.shooter.ui.actors::ProtonsBomb">
				<scmin><![CDATA[.5]]></scmin>
				<scmax><![CDATA[.8]]></scmax>
				<spmin><![CDATA[.8]]></spmin>
				<spmax><![CDATA[4]]></spmax>
				<value><![CDATA[+01]]></value> 
				<coef><![CDATA[0]]></coef>
				<sound><![CDATA[fxProtonsBomb]]></sound>
			</asset>
			<asset id="threats" controller="activia.simon.shooter.ui.actors::ThreatsBomb">
				<scmin><![CDATA[.5]]></scmin>
				<scmax><![CDATA[.8]]></scmax>
				<spmin><![CDATA[1]]></spmin>
				<spmax><![CDATA[2]]></spmax>
				<value><![CDATA[-02]]></value>
				<coef><![CDATA[4]]></coef>
				<sound><![CDATA[fxThreastsBomb]]></sound>
			</asset>
		</assets>
	</actors>
</recordset>;

		public static const XML_LOCALIZATION:XML = <recordset>      
	<lbHeaderBarTwoExit>
		<label><![CDATA[Salir]]></label>
	</lbHeaderBarTwoExit>		
	<lbHeaderBarTwoInstructions>
		<label><![CDATA[Instrucciones]]></label>
	</lbHeaderBarTwoInstructions>	
	<lbHeaderBarTwoTime>
		<label><![CDATA[{1}:{2}]]></label>
	</lbHeaderBarTwoTime>	
	<lbHeaderBarTwoScore>
		<label><![CDATA[x@ddd@]]></label>
		<replace id="@ddd@">score_value</replace>
	</lbHeaderBarTwoScore>
	<lbGHomePlayTheGame>
		<label><![CDATA[EMPEZÁ A JUGAR]]></label>     
	</lbGHomePlayTheGame>
	<lbGHomeInstructions>
		<label><![CDATA[INSTRUCCIONES]]></label>      
	</lbGHomeInstructions>	
	<lbGHomeTitle1>
		<label><![CDATA[DECLARÁ LA PAZ<br/>EN TU ESTÓMAGO]]></label>
	</lbGHomeTitle1>	
	<lbGHomeTitle2>
		<label><![CDATA[Desactivá las bombas de protones<br/>y combatí la acidez frecuente...]]></label>
	</lbGHomeTitle2>
	<lbGHomeViewMap>
		<label><![CDATA[CONOCÉ EL MAPA<br/>DE LA ACIDEZ<br/>FRECUENTE]]></label>
	</lbGHomeViewMap>
	<lbGInstructionsPlay>
		<label><![CDATA[JUGAR]]></label> 
	</lbGInstructionsPlay>
	<lbGInstructionsNext>
		<label><![CDATA[SIGUIENTE]]></label> 
	</lbGInstructionsNext>
	<lbGInstructionsPrev>
		<label><![CDATA[ANTERIOR]]></label> 
	</lbGInstructionsPrev>	
	<lbGInstructionsS1Title>
		<label><![CDATA[INSTRUCCIONES]]></label> 
	</lbGInstructionsS1Title>	
	<lbGInstructionsS1P1>
		<title><![CDATA[EL OBJETIVO:]]></title> 
		<detail><![CDATA[Desactivar la mayor cantidad de bombas de protones que despiden ácido<br/>en el estómago, en el menor tiempo posible, para lograr la paz en tu estómago.]]></detail> 
	</lbGInstructionsS1P1>	
	<lbGInstructionsS1P2>
		<title><![CDATA[Aziatop:]]></title> 
		<detail><![CDATA[Cierra las bombas que están abiertas despidiendo ácido.]]></detail> 
	</lbGInstructionsS1P2>	
	<lbGInstructionsS1P3>
		<title><![CDATA[Bombas de protones abiertas:]]></title> 
		<detail><![CDATA[Desactivarlas equivale a 1 punto (para desactivarlas deberás hacer click sobre las bombas).]]></detail> 
	</lbGInstructionsS1P3>	
	<lbGInstructionsS1P4>
		<title><![CDATA[Ácido:]]></title> 
		<detail><![CDATA[Causante de la acidez frecuente despedido por las bombas abiertas.]]></detail> 
	</lbGInstructionsS1P4>	
	<lbGInstructionsS1P5>
		<title><![CDATA[Amenazas:]]></title> 
		<detail><![CDATA[Si clickeás sobre los íconos de las<br/>amenazas, restás 2 puntos.]]></detail> 
	</lbGInstructionsS1P5>	
	<lbGInstructionsS2P1>
		<title><![CDATA[Aliados:]]></title> 
		<detail><![CDATA[Si clickeás sobre los íconos de los aliados, neutralizás las bombas<br/>que en ese momento estén abiertas.]]></detail>
	</lbGInstructionsS2P1>	
	<lbGInstructionsS2P2>
		<title><![CDATA[Barra de síntomas:]]></title> 
		<detail><![CDATA[Cuantas menos bombas desactives, más síntomas aparecerán.]]></detail> 
		<detai2><![CDATA[1- Regurgitación ácida<br/>2- Sensación de ardor y quemazón<br/>3- Dolor en la boca del estómago.]]></detai2> 
	</lbGInstructionsS2P2>	
	<lbGameInstructions>
		<label><![CDATA[INSTRUCCIONES]]></label>      
	</lbGameInstructions>
	<lbGameExit>
		<label><![CDATA[SALIR]]></label>
	</lbGameExit>
	<lbGOverScoreRegiste>
		<label><![CDATA[Ingresá tu resultado en el Ranking]]></label>      
	</lbGOverScoreRegiste>
	<lbGOverPlayAgain>
		<label><![CDATA[Volvé a jugar]]></label>      
	</lbGOverPlayAgain>
	<lbGOverTitle>
		<label><![CDATA[DESACTIVASTE]]></label>
	</lbGOverTitle>	
	<lbGOverScore>
		<label><![CDATA[@score@ bombas]]></label>
		<replace id="@score@">score_value</replace> <!-- DATALAYER -->
	</lbGOverScore>
	<lbGExitQuestion>
		<label><![CDATA[¿Deseas abandonar<br/>el juego?]]></label>      
	</lbGExitQuestion>		
	<lbGExitYes>
		<label size="17.5" y="-4"><![CDATA[SI]]></label>      
	</lbGExitYes>	
	<lbGExitNo>
		<label size="17.5" y="-4"><![CDATA[NO]]></label>      
	</lbGExitNo>
	<lbGScoreRegisteTitle>
		<label><![CDATA[INGRESÁ TU NOMBRE]]></label>
	</lbGScoreRegisteTitle>	
	<lbGScoreRegisteSend>
		<label><![CDATA[Ingresar]]></label>
	</lbGScoreRegisteSend>
	<lbGScoreRegisteError>
		<label><![CDATA[]]></label>
		<validateName><![CDATA[Completá tu nombre.]]></validateName>
		<sending><![CDATA[Tu puntaje está siendo enviado, aguardá un instante.]]></sending>
		<success><![CDATA[Tu puntaje fue recibido exitosamente.]]></success>
		<error1><![CDATA[Tu puntaje no pudo ser enviado, volvé a intentar.]]></error1>
		<error2><![CDATA[El servidor no responde, volvé a intentar más tarde.]]></error2>
		<uncontrolledError><![CDATA[Error no controlado.]]></uncontrolledError>
	</lbGScoreRegisteError>
	<lbGRankingTitle>
		<label><![CDATA[RANKING]]></label>
	</lbGRankingTitle>
	<lbGRankingSocialNetworkTitle>
		<label><![CDATA[Publicá el resultado en tus redes sociales.]]></label>
	</lbGRankingSocialNetworkTitle>	
	<lbGRankingFacebookShare>
		<label><![CDATA[COMPARTIR]]></label>
	</lbGRankingFacebookShare>	
	<lbGRankingFacebookWall>
		<label><![CDATA[PUBLICÁ TU<br/>RESULTADO]]></label>
	</lbGRankingFacebookWall>	
	<lbGRankingLoading>
		<label><![CDATA[Cargando Datos...]]></label>
		<error1><![CDATA[Los datos no se encuentran disponibles.]]></error1>
		<uncontrolledError><![CDATA[Error no controlado.]]></uncontrolledError>
	</lbGRankingLoading>
	<lbGRankingCell offset="-5">
		<name><![CDATA[{1}]]></name>
		<position><![CDATA[{1} -]]></position>
		<score><![CDATA[ x {1}]]></score>
	</lbGRankingCell>	
</recordset>;
		
	}

}