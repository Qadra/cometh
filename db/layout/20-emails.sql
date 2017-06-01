CREATE TABLE `emails` (
	  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
	  `email` varchar(80) NOT NULL,
	  `user` int(10) unsigned NOT NULL,
	  PRIMARY KEY (`id`),
	  UNIQUE KEY `email` (`email`),
	  KEY `user` (`user`),
	  CONSTRAINT `emails_ibfk_1` FOREIGN KEY (`user`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
