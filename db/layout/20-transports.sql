CREATE TABLE `transports` (
	  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
	  `domain` varchar(128) NOT NULL DEFAULT '',
	  `transport` varchar(128) NOT NULL DEFAULT '',
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `domain` (`domain`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
