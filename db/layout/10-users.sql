CREATE TABLE `users` (
	  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
	  `name` varchar(100) DEFAULT NULL,
	  `email` varchar(80) NOT NULL,
	  `password` char(124) NOT NULL,
	  `quota` int(10) DEFAULT '0',
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
