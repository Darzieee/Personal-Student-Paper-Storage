SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `dbuser` (
  `id` longtext NOT NULL,
  `nrp` longtext NOT NULL,
  `name` longtext NOT NULL,
  `email` longtext NOT NULL,
  `password` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;