CREATE TABLE `domains` (
	  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
	  `domain` varchar(50) NOT NULL,
	  `virtual` tinyint(1) NOT NULL DEFAULT '0',
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `domain` (`domain`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
