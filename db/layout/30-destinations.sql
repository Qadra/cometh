CREATE TABLE `destinations` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `destination` varchar(80) NOT NULL,
  `forwarding` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `destination` (`destination`,`forwarding`),
  KEY `forwarding` (`forwarding`),
  CONSTRAINT `destinations_ibfk_1` FOREIGN KEY (`forwarding`) REFERENCES `forwardings` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8
