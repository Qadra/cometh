CREATE TABLE `forwardings` (
	  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
	  `local` varchar(80) NOT NULL,
	  `domain` int(10) unsigned NOT NULL,
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `local` (`local`,`domain`),
	  KEY `domain` (`domain`),
	  CONSTRAINT `forwardings_ibfk_1` FOREIGN KEY (`domain`) REFERENCES `domains` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8
