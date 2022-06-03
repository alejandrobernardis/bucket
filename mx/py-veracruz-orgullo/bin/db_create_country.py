#!/usr/bin/env python
# -*- coding: utf-8 -*-
import db_cnx

# imports
try:
    import settings
    from mx.dip.voj.models.countries import Country

except:
    exit(u'Ups!, no están todos los módulos.')


countries_list = ((1,u'Afganistán'),(2,u'Albania'),(3,u'Argelia'),(4,u'Samoa Americana'),(5,u'Andorra'),(6,u'Angola'),
                  (7,u'Anguilla'),(8,u'Antártida'),(9,u'Antigua y Barbuda'),(10,u'Argentina'),(11,u'Armenia'),
                  (12,u'Aruba'),(13,u'Australia'),(14,u'Austria'),(15,u'Azerbaiyán'),(16,u'Bahamas'),(17,u'Bahrein'),
                  (18,u'Bangladesh'),(19,u'Barbados'),(20,u'Bielorrusia'),(21,u'Bélgica'),(22,u'Belice'),(23,u'Benín'),
                  (24,u'Bermudas'),(25,u'Bután'),(26,u'Bolivia'),(27,u'Bosnia-Herzegovina'),(28,u'Botswana'),
                  (29,u'Brasil'),(30,u'Brunei Darussalam'),(31,u'Bulgaria'),(32,u'Burkina Faso'),(33,u'Burundi'),
                  (34,u'Camboya'),(35,u'Camerún'),(36,u'Canadá'),(37,u'Cabo Verde'),(38,u'Islas Caimán'),
                  (39,u'República Centroafricana'),(40,u'Chad'),(41,u'Chile'),(42,u'China'),(43,u'Isla De Navidad'),
                  (44,u'Islas Cocos'),(45,u'Colombia'),(46,u'Comores'),(47,u'República Democrática del Congo'),
                  (48,u'República del Congo'),(49,u'Islas Cook'),(50,u'Costa Rica'),(51,u'Costa de Marfil'),
                  (52,u'Croacia'),(53,u'Cuba'),(54,u'Chipre'),(55,u'República Checa'),(56,u'Dinamarca'),
                  (57,u'Djibouti, Yibuti'),(58,u'Dominica'),(59,u'Dominicana, República'),(60,u'Timor Oriental'),
                  (61,u'Ecuador'),(62,u'Egipto'),(63,u'El Salvador'),(64,u'Guinea Ecuatorial'),(65,u'Eritrea'),
                  (66,u'Estonia'),(67,u'Etiopía'),(68,u'Islas Malvinas'),(69,u'Islas Feroe'),(70,u'Fiyi'),
                  (71,u'Finlandia'),(72,u'Francia'),(73,u'Guayana Francesa'),(74,u'Polinesia Francesa'),
                  (75,u'Tierras Australes y Antárticas Francesas'),(76,u'Gabón'),(77,u'Gambia'),(78,u'Georgia'),
                  (79,u'Alemania'),(80,u'Ghana'),(81,u'Gibraltar'),(82,u'Gran Bretaña'),(83,u'Grecia'),
                  (84,u'Groenlandia'),(85,u'Granada'),(86,u'Guadalupe'),(87,u'Guam'),(88,u'Guatemala'),
                  (89,u'República Guinea'),(90,u'Guinea Bissau'),(91,u'Guyana'),(92,u'Haiti'),
                  (93,u'Ciudad del Vaticano'),(94,u'Honduras'),(95,u'Hong Kong'),(96,u'Hungría'),(97,u'Islandia'),
                  (98,u'India'),(99,u'Indonesia'),(100,u'Irán'),(101,u'Iraq'),(102,u'Irlanda'),(103,u'Israel'),
                  (104,u'Italia'),(105,u'Jamaica'),(106,u'Japón'),(107,u'Jordania'),(108,u'Kazajstán'),(109,u'Kenia'),
                  (110,u'Kiribati'),(111,u'Corea del Norte'),(112,u'Corea del Sur'),(113,u'Kosovo'),
                  (114,u'Europa del Sur'),(115,u'Kuwait'),(116,u'Kirguistán'),(117,u'Laos'),(118,u'Letonia'),
                  (119,u'Líbano'),(120,u'Lesotho'),(121,u'Liberia'),(122,u'Libia'),(123,u'Liechtenstein'),
                  (124,u'Lituania'),(125,u'Luxemburgo'),(126,u'Macao'),(127,u'Macedonia'),(128,u'Madagascar'),
                  (129,u'Malawi'),(130,u'Malasia'),(131,u'Maldivas'),(132,u'Malí'),(133,u'Malta'),
                  (134,u'Islas Marshall'),(135,u'Martinica'),(136,u'Mauritania'),(137,u'Mauricio'),(138,u'Mayotte'),
                  (139,u'México'),(140,u'Micronesia'),(141,u'Moldavia'),(142,u'Mónaco'),(143,u'Mongolia'),
                  (144,u'Montenegro'),(145,u'Montserrat'),(146,u'Marruecos'),(147,u'Mozambique'),
                  (148,u'Myanmar, Birmania'),(149,u'Namibia'),(150,u'Nauru'),(151,u'Nepal'),
                  (152,u'Países Bajos, Holanda'),(153,u'Antillas Holandesas'),(154,u'Nueva Caledonia'),
                  (155,u'Nueva Zelanda'),(156,u'Nicaragua'),(157,u'Niger'),(158,u'Nigeria'),(159,u'Niue'),
                  (160,u'Marianas del Norte'),(161,u'Noruega'),(162,u'Omán'),(163,u'Pakistán'),(164,u'Palau'),
                  (165,u'Palestina'),(166,u'Panamá'),(167,u'Papúa-Nueva Guinea'),(168,u'Paraguay'),(169,u'Perú'),
                  (170,u'Filipinas'),(171,u'Isla Pitcairn'),(172,u'Polonia'),(173,u'Portugal'),(174,u'Puerto Rico'),
                  (175,u'Qatar'),(176,u'Reunión'),(177,u'Rumanía'),(178,u'Federación Rusa'),(179,u'Ruanda'),
                  (180,u'San Cristobal y Nevis'),(181,u'Santa Lucía'),(182,u'San Vincente y Granadinas'),(183,u'Samoa'),
                  (184,u'San Marino'),(185,u'Santo Tomé y Príncipe'),(186,u'Arabia Saudita'),(187,u'Senegal'),
                  (188,u'Serbia'),(189,u'Seychelles'),(190,u'Sierra Leona'),(191,u'Singapur'),(192,u'Eslovaquia'),
                  (193,u'Eslovenia'),(194,u'Islas Salomón'),(195,u'Somalia'),(196,u'Sudáfrica'),(197,u'Sudán del Sur'),
                  (198,u'España'),(199,u'Sri Lanka'),(200,u'Sudán'),(201,u'Surinam'),(202,u'Swazilandia'),
                  (203,u'Suecia'),(204,u'Suiza'),(205,u'Siria'),(206,u'Taiwan'),(207,u'Tadjikistan'),(208,u'Tanzania'),
                  (209,u'Tailandia'),(210,u'Tíbet'),(211,u'Timor Oriental'),(212,u'Togo'),(213,u'Tokelau'),
                  (214,u'Tonga'),(215,u'Trinidad y Tobago'),(216,u'Túnez'),(217,u'Turquía'),(218,u'Turkmenistan'),
                  (219,u'Islas Turcas y Caicos'),(220,u'Tuvalu'),(221,u'Uganda'),(222,u'Ucrania'),
                  (223,u'Emiratos Árabes Unidos'),(224,u'Reino Unido'),(225,u'Estados Unidos'),(226,u'Uruguay'),
                  (227,u'Uzbekistán'),(228,u'Vanuatu'),(229,u'Ciudad del Vaticano'),(230,u'Venezuela'),(231,u'Vietnam'),
                  (232,u'Islas Virgenes Británicas'),(233,u'Islas Virgenes Americanas'),(234,u'Wallis y Futuna'),
                  (235,u'Sáhara Occidental'),(236,u'Yemen'),(237,u'Zambia'),(238,u'Zimbabwe'))

Country.drop_collection()

for _pid, _name in countries_list:
    country = Country()
    country.pid = _pid
    country.name = _name
    country.available = True
    country.enabled = True
    country.save()

print Country.objects.count()