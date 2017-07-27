CREATE TABLE `forwardings` (
	  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
	  `source` varchar(255) NOT NULL,
	  `destination` text NOT NULL,
	  PRIMARY KEY (`id`),
	  KEY `source` (`source`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
