CREATE TABLE `users` (
	  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
	  `name` varchar(100) DEFAULT NULL,
	  `email` varchar(80) NOT NULL,
	  `password` char(106) NOT NULL,
	  `quota` int(10) DEFAULT '0',
	  PRIMARY KEY (`id`),
	  KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
