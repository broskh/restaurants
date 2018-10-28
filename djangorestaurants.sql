-- START INIT
CREATE schema djangorestaurants;
USE djangorestaurants;
CREATE USER 'userrestaurants'@'localhost' IDENTIFIED BY 'restaurants2018';
GRANT ALL PRIVILEGES ON djangorestaurants.* TO 'userrestaurants'@'localhost' WITH GRANT OPTION;
GRANT ALL ON test_djangorestaurants.* TO 'userrestaurants'@'localhost';
-- END INIT

-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Creato il: Ago 22, 2018 alle 14:52
-- Versione del server: 5.7.23-0ubuntu0.16.04.1
-- Versione PHP: 7.0.31-1+ubuntu16.04.1+deb.sury.org+1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `djangorestaurants`
--

-- --------------------------------------------------------

--
-- Struttura della tabella `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(80) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struttura della tabella `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struttura della tabella `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add booking', 1, 'add_booking'),
(2, 'Can change booking', 1, 'change_booking'),
(3, 'Can delete booking', 1, 'delete_booking'),
(4, 'Can add menu voice', 2, 'add_menuvoice'),
(5, 'Can change menu voice', 2, 'change_menuvoice'),
(6, 'Can delete menu voice', 2, 'delete_menuvoice'),
(7, 'Can add menu category', 3, 'add_menucategory'),
(8, 'Can change menu category', 3, 'change_menucategory'),
(9, 'Can delete menu category', 3, 'delete_menucategory'),
(10, 'Can add kitchen type', 4, 'add_kitchentype'),
(11, 'Can change kitchen type', 4, 'change_kitchentype'),
(12, 'Can delete kitchen type', 4, 'delete_kitchentype'),
(13, 'Can add restaurant image', 5, 'add_restaurantimage'),
(14, 'Can change restaurant image', 5, 'change_restaurantimage'),
(15, 'Can delete restaurant image', 5, 'delete_restaurantimage'),
(16, 'Can add user', 6, 'add_user'),
(17, 'Can change user', 6, 'change_user'),
(18, 'Can delete user', 6, 'delete_user'),
(19, 'Can add restaurant', 7, 'add_restaurant'),
(20, 'Can change restaurant', 7, 'change_restaurant'),
(21, 'Can delete restaurant', 7, 'delete_restaurant'),
(22, 'Can add service', 8, 'add_service'),
(23, 'Can change service', 8, 'change_service'),
(24, 'Can delete service', 8, 'delete_service'),
(25, 'Can add log entry', 9, 'add_logentry'),
(26, 'Can change log entry', 9, 'change_logentry'),
(27, 'Can delete log entry', 9, 'delete_logentry'),
(28, 'Can add permission', 10, 'add_permission'),
(29, 'Can change permission', 10, 'change_permission'),
(30, 'Can delete permission', 10, 'delete_permission'),
(31, 'Can add group', 11, 'add_group'),
(32, 'Can change group', 11, 'change_group'),
(33, 'Can delete group', 11, 'delete_group'),
(34, 'Can add content type', 12, 'add_contenttype'),
(35, 'Can change content type', 12, 'change_contenttype'),
(36, 'Can delete content type', 12, 'delete_contenttype'),
(37, 'Can add session', 13, 'add_session'),
(38, 'Can change session', 13, 'change_session'),
(39, 'Can delete session', 13, 'delete_session');

-- --------------------------------------------------------

--
-- Struttura della tabella `booking_booking`
--

CREATE TABLE `booking_booking` (
  `id` int(11) NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `n_places` int(10) UNSIGNED NOT NULL,
  `state` smallint(5) UNSIGNED NOT NULL,
  `client_id` int(11) NOT NULL,
  `restaurant_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `booking_booking`
--

INSERT INTO `booking_booking` (`id`, `start_time`, `end_time`, `n_places`, `state`, `client_id`, `restaurant_id`) VALUES
(1, '2018-08-31 20:00:00.000000', '2018-08-31 22:00:00.000000', 4, 1, 4, 1),
(2, '2018-08-15 12:30:00.000000', '2018-08-15 14:30:00.000000', 2, 1, 2, 2),
(3, '2018-09-12 19:00:00.000000', '2018-09-12 20:00:00.000000', 10, 1, 2, 4),
(4, '2018-09-12 19:30:00.000000', '2018-09-12 20:30:00.000000', 195, 0, 4, 4);

-- --------------------------------------------------------

--
-- Struttura della tabella `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2018-08-22 09:03:43.073245', '1', 'Italiana', 1, '[{"added": {}}]', 4, 1),
(2, '2018-08-22 09:03:49.083550', '2', 'Pesce', 1, '[{"added": {}}]', 4, 1),
(3, '2018-08-22 09:04:01.646129', '3', 'Giapponese', 1, '[{"added": {}}]', 4, 1),
(4, '2018-08-22 09:04:07.506392', '4', 'Cinese', 1, '[{"added": {}}]', 4, 1),
(5, '2018-08-22 09:04:53.153252', '1', 'Tradizionale', 2, '[{"changed": {"fields": ["value"]}}]', 4, 1),
(6, '2018-08-22 09:05:02.472205', '5', 'Pizza', 1, '[{"added": {}}]', 4, 1),
(7, '2018-08-22 09:05:14.122710', '1', 'Eventi sportivi in TV', 1, '[{"added": {}}]', 8, 1),
(8, '2018-08-22 09:05:16.927207', '2', 'Free Wi-Fi', 1, '[{"added": {}}]', 8, 1),
(9, '2018-08-22 09:05:20.783899', '3', 'Spazio giochi per bambini', 1, '[{"added": {}}]', 8, 1),
(10, '2018-08-22 09:05:40.660089', '4', 'Aria condizionata', 1, '[{"added": {}}]', 8, 1),
(11, '2018-08-22 09:07:31.724158', '2', 'ugofoscolo', 1, '[{"added": {}}]', 6, 1),
(12, '2018-08-22 09:14:29.450574', '1', 'Pizzeria dei Mille', 1, '[{"added": {}}, {"added": {"object": "download.jpeg", "name": "restaurant image"}}, {"added": {"object": "download_1.jpeg", "name": "restaurant image"}}, {"added": {"object": "Pizze", "name": "menu category"}}, {"added": {"object": "Bevande", "name": "menu category"}}]', 7, 1),
(13, '2018-08-22 09:16:38.740737', '3', 'giuseppegaribaldi', 1, '[{"added": {}}]', 6, 1),
(14, '2018-08-22 09:17:41.623788', '1', 'Margherita-Pizze: Pizzeria dei Mille', 1, '[{"added": {}}]', 2, 1),
(15, '2018-08-22 09:17:50.113228', '2', 'Diavola-Pizze: Pizzeria dei Mille', 1, '[{"added": {}}]', 2, 1),
(16, '2018-08-22 09:18:06.104544', '3', 'Patatine Fritte-Pizze: Pizzeria dei Mille', 1, '[{"added": {}}]', 2, 1),
(17, '2018-08-22 09:18:17.086974', '4', 'Acqua-Bevande: Pizzeria dei Mille', 1, '[{"added": {}}]', 2, 1),
(18, '2018-08-22 09:51:58.803349', '6', 'l_6301_nuovi-ristoranti-roma-primavera-2017.jpg', 1, '[{"added": {}}]', 5, 1),
(19, '2018-08-22 09:52:39.578456', '6', 'Bevande: I Malavoglia', 1, '[{"added": {}}, {"added": {"object": "Acqua naturale-Bevande: I Malavoglia", "name": "menu voice"}}]', 3, 1),
(20, '2018-08-22 10:00:13.483717', '1', 'Booking object', 1, '[{"added": {}}]', 1, 1),
(21, '2018-08-22 10:01:43.482752', '2', 'Booking object', 1, '[{"added": {}}]', 1, 1);

-- --------------------------------------------------------

--
-- Struttura della tabella `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(9, 'admin', 'logentry'),
(11, 'auth', 'group'),
(10, 'auth', 'permission'),
(1, 'booking', 'booking'),
(12, 'contenttypes', 'contenttype'),
(13, 'sessions', 'session'),
(4, 'user_management', 'kitchentype'),
(3, 'user_management', 'menucategory'),
(2, 'user_management', 'menuvoice'),
(7, 'user_management', 'restaurant'),
(5, 'user_management', 'restaurantimage'),
(8, 'user_management', 'service'),
(6, 'user_management', 'user');

-- --------------------------------------------------------

--
-- Struttura della tabella `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2018-08-22 08:58:53.835492'),
(2, 'contenttypes', '0002_remove_content_type_name', '2018-08-22 08:58:53.877818'),
(3, 'auth', '0001_initial', '2018-08-22 08:58:54.066625'),
(4, 'auth', '0002_alter_permission_name_max_length', '2018-08-22 08:58:54.076509'),
(5, 'auth', '0003_alter_user_email_max_length', '2018-08-22 08:58:54.088485'),
(6, 'auth', '0004_alter_user_username_opts', '2018-08-22 08:58:54.112429'),
(7, 'auth', '0005_alter_user_last_login_null', '2018-08-22 08:58:54.119627'),
(8, 'auth', '0006_require_contenttypes_0002', '2018-08-22 08:58:54.122538'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2018-08-22 08:58:54.130850'),
(10, 'auth', '0008_alter_user_username_max_length', '2018-08-22 08:58:54.141155'),
(11, 'user_management', '0001_initial', '2018-08-22 08:58:54.790409'),
(12, 'admin', '0001_initial', '2018-08-22 08:58:54.890463'),
(13, 'admin', '0002_logentry_remove_auto_add', '2018-08-22 08:58:54.906792'),
(14, 'user_management', '0002_auto_20180822_0858', '2018-08-22 08:58:54.918685'),
(15, 'booking', '0001_initial', '2018-08-22 08:58:55.001277'),
(16, 'sessions', '0001_initial', '2018-08-22 08:58:55.025298'),
(17, 'user_management', '0003_auto_20180822_1130', '2018-08-22 11:30:22.646188');

-- --------------------------------------------------------

--
-- Struttura della tabella `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('6jzumzs4yxwjyatgattabaumdw670bi0', 'YWRiNjhkNmI2YTg2ZjY4MGIzNjBkYjQ1ZTc2Y2U1NDUyNDM4NTFiZTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJmMDI3ZmNlYWQxMzExY2QwYjMxODczMWNjMjY1YjJmMDFkMTdmYjM2In0=', '2018-09-05 10:05:08.642880');

-- --------------------------------------------------------

--
-- Struttura della tabella `user_management_kitchentype`
--

CREATE TABLE `user_management_kitchentype` (
  `id` int(11) NOT NULL,
  `value` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `user_management_kitchentype`
--

INSERT INTO `user_management_kitchentype` (`id`, `value`) VALUES
(1, 'Tradizionale'),
(2, 'Pesce'),
(3, 'Giapponese'),
(4, 'Cinese'),
(5, 'Pizza');

-- --------------------------------------------------------

--
-- Struttura della tabella `user_management_menucategory`
--

CREATE TABLE `user_management_menucategory` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `restaurant_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `user_management_menucategory`
--

INSERT INTO `user_management_menucategory` (`id`, `name`, `restaurant_id`) VALUES
(1, 'Pizze', 1),
(2, 'Bevande', 1),
(3, 'Primi', 2),
(4, 'Secondi', 2),
(5, 'Hosomaki', 3),
(6, 'Bevande', 5);

-- --------------------------------------------------------

--
-- Struttura della tabella `user_management_menuvoice`
--

CREATE TABLE `user_management_menuvoice` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `price` double NOT NULL,
  `menu_category_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `user_management_menuvoice`
--

INSERT INTO `user_management_menuvoice` (`id`, `name`, `price`, `menu_category_id`) VALUES
(1, 'Margherita', 5, 1),
(2, 'Diavola', 6, 1),
(3, 'Patatine Fritte', 6.5, 1),
(4, 'Acqua', 2, 2),
(5, 'Spaghetti alle vongole', 8.5, 3),
(6, 'Risotto allo scoglio', 9, 3),
(7, 'Frittura mista', 14, 4),
(8, 'Salmone', 3, 5),
(9, 'Orata', 3.5, 5),
(10, 'Acqua naturale', 1.5, 6);

-- --------------------------------------------------------

--
-- Struttura della tabella `user_management_restaurant`
--

CREATE TABLE `user_management_restaurant` (
  `id` int(11) NOT NULL,
  `name` varchar(200) NOT NULL,
  `city` varchar(150) NOT NULL,
  `address` varchar(150) NOT NULL,
  `n_places` int(10) UNSIGNED NOT NULL,
  `booking_duration` int(10) UNSIGNED NOT NULL,
  `longitude` double DEFAULT NULL,
  `latitude` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `user_management_restaurant`
--

INSERT INTO `user_management_restaurant` (`id`, `name`, `city`, `address`, `n_places`, `booking_duration`, `longitude`, `latitude`) VALUES
(1, 'Pizzeria dei Mille', 'San Cesario sul Panaro', 'Via della Meccanica, 16', 100, 120, 11.0279393, 44.5894158),
(2, 'Da Alessandro', 'Vignola', 'Via Baracchini, 95', 80, 120, 11.0061737, 44.4856207),
(3, 'L\'Infinito', 'Savignano sul Panaro', 'Via Claudia, 5569', 60, 90, 11.0197113, 44.4691969),
(4, 'Il Fu Mattia Pascal', 'Modena', 'Via Campi, 213/a', 200, 60, 10.9435366, 44.6320812),
(5, 'I Malavoglia', 'San Donnino', 'Via Gherbella, 454/a', 75, 60, 10.96845, 44.58539);

-- --------------------------------------------------------

--
-- Struttura della tabella `user_management_restaurantimage`
--

CREATE TABLE `user_management_restaurantimage` (
  `id` int(11) NOT NULL,
  `image` varchar(100) NOT NULL,
  `restaurant_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `user_management_restaurantimage`
--

INSERT INTO `user_management_restaurantimage` (`id`, `image`, `restaurant_id`) VALUES
(1, '2018/08/22/09/00/13/download.jpeg', 1),
(2, '2018/08/22/09/00/13/download_1.jpeg', 1),
(3, '2018/08/22/09/23/46/gauchos-ristoranti-sala-f4b55.jpg', 2),
(4, '2018/08/22/09/23/46/images.jpeg', 2),
(5, '2018/08/22/09/23/46/l_5283_ristoranti-all-aperto-milano.jpg', 2),
(6, '2018/08/22/09/40/25/l_6301_nuovi-ristoranti-roma-primavera-2017.jpg', 4);

-- --------------------------------------------------------

--
-- Struttura della tabella `user_management_restaurant_kitchen_types`
--

CREATE TABLE `user_management_restaurant_kitchen_types` (
  `id` int(11) NOT NULL,
  `restaurant_id` int(11) NOT NULL,
  `kitchentype_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `user_management_restaurant_kitchen_types`
--

INSERT INTO `user_management_restaurant_kitchen_types` (`id`, `restaurant_id`, `kitchentype_id`) VALUES
(1, 1, 5),
(2, 2, 1),
(3, 2, 2),
(4, 3, 3),
(5, 3, 4),
(6, 4, 1),
(7, 5, 5);

-- --------------------------------------------------------

--
-- Struttura della tabella `user_management_restaurant_services`
--

CREATE TABLE `user_management_restaurant_services` (
  `id` int(11) NOT NULL,
  `restaurant_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `user_management_restaurant_services`
--

INSERT INTO `user_management_restaurant_services` (`id`, `restaurant_id`, `service_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 4),
(4, 2, 2),
(5, 2, 4),
(7, 4, 2),
(8, 4, 3),
(9, 5, 4);

-- --------------------------------------------------------

--
-- Struttura della tabella `user_management_service`
--

CREATE TABLE `user_management_service` (
  `id` int(11) NOT NULL,
  `value` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `user_management_service`
--

INSERT INTO `user_management_service` (`id`, `value`) VALUES
(1, 'Eventi sportivi in TV'),
(2, 'Free Wi-Fi'),
(3, 'Spazio giochi per bambini'),
(4, 'Aria condizionata');

-- --------------------------------------------------------

--
-- Struttura della tabella `user_management_user`
--

CREATE TABLE `user_management_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `user_type` smallint(5) UNSIGNED DEFAULT NULL,
  `restaurant_information_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dump dei dati per la tabella `user_management_user`
--

INSERT INTO `user_management_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `user_type`, `restaurant_information_id`) VALUES
(1, 'pbkdf2_sha256$36000$h8SgiCENUfUx$U4aQ23PgnsQouD48FZizSxQ2ZLX7ygedVUdl4M/X7WA=', '2018-08-22 10:05:08.640692', 1, 'admin', 'Alessio', 'Scheri', 'alessio.scheri@gmail.com', 1, 1, '2018-08-22 09:01:10.660676', NULL, NULL),
(2, 'pbkdf2_sha256$36000$RvFJbFQJ1l6Y$CqTyiLmxsOfuI5Wggw2vQvKnVmqBm+qDoHfWW7awSU8=', '2018-08-22 10:04:50.571760', 0, 'ugofoscolo', 'Ugo', 'Foscolo', 'ugo.foscolo@mail.it', 0, 1, '2018-08-22 09:06:18.000000', 1, NULL),
(3, 'pbkdf2_sha256$36000$EuzR1YiyYQ9k$25fFlfnVArty8tgRN5/HNwOPuwyxGvpGrH4+h2YzSTA=', NULL, 0, 'giuseppegaribaldi', 'Giuseppe', 'Garibaldi', 'giuseppe.garibaldi@mail.it', 0, 1, '2018-08-22 09:07:31.000000', 2, 1),
(4, 'pbkdf2_sha256$36000$jlYtDF634kWq$X7hkvXIFd2awgVCgYQbP7Ekj+lyXlsho56M2FbAaLzk=', '2018-08-22 10:03:46.281296', 0, 'giovannipascoli', 'GIovanni', 'Pascoli', 'giovanni.pascoli@mail.it', 0, 1, '2018-08-22 09:27:26.515600', 1, NULL),
(5, 'pbkdf2_sha256$36000$lPZDd8fAqQ1n$KpXNbPii8YW4jNb26EWnjdPAsm3yil1JDo40HUk1MEg=', '2018-08-22 09:29:50.505675', 0, 'alessandromanzoni', 'Alessandro', 'Manzoni', 'alessandro.manzoni@mail.it', 0, 1, '2018-08-22 09:29:49.866382', 2, 2),
(6, 'pbkdf2_sha256$36000$JbQgyeRFPnKc$0MwX+eBNUVH+XS4lvMIZsSa0dLV76y+dK6L5pw9/5lc=', '2018-08-22 09:36:57.915355', 0, 'giacomoleopardi', 'Giacomo', 'Leopardi', 'giacomo.leopardi@mail.it', 0, 1, '2018-08-22 09:36:57.224592', 2, 3),
(7, 'pbkdf2_sha256$36000$nmvXT5jUAxyz$0LZnwyVX11LSeRXjA12oBxdgcKmtg4JH791B0ddbymc=', '2018-08-22 09:46:01.781761', 0, 'luigipirandello', 'Luigi', 'Pirandello', 'luigi.pirandello@mail.it', 0, 1, '2018-08-22 09:46:00.924722', 2, 4),
(8, 'pbkdf2_sha256$36000$0knB0VWywM3A$oOzwsefG+AtkMdbpM5FlJrFcFFsqTn8MbFI1zOf1ZcQ=', '2018-08-22 09:50:34.798447', 0, 'giovanniverga', 'Giovanni', 'Verga', 'giovanni.verga@mail.it', 0, 1, '2018-08-22 09:50:34.053337', 2, 5);

-- --------------------------------------------------------

--
-- Struttura della tabella `user_management_user_groups`
--

CREATE TABLE `user_management_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struttura della tabella `user_management_user_user_permissions`
--

CREATE TABLE `user_management_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indici per le tabelle scaricate
--

--
-- Indici per le tabelle `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indici per le tabelle `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indici per le tabelle `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indici per le tabelle `booking_booking`
--
ALTER TABLE `booking_booking`
  ADD PRIMARY KEY (`id`),
  ADD KEY `booking_booking_client_id_4b0e9d36_fk_user_management_user_id` (`client_id`),
  ADD KEY `booking_booking_restaurant_id_4188bc98_fk_user_mana` (`restaurant_id`);

--
-- Indici per le tabelle `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_user_management_user_id` (`user_id`);

--
-- Indici per le tabelle `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indici per le tabelle `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indici per le tabelle `user_management_kitchentype`
--
ALTER TABLE `user_management_kitchentype`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `user_management_menucategory`
--
ALTER TABLE `user_management_menucategory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_management_menu_restaurant_id_30692d9d_fk_user_mana` (`restaurant_id`);

--
-- Indici per le tabelle `user_management_menuvoice`
--
ALTER TABLE `user_management_menuvoice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_management_menu_menu_category_id_109e7e45_fk_user_mana` (`menu_category_id`);

--
-- Indici per le tabelle `user_management_restaurant`
--
ALTER TABLE `user_management_restaurant`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `user_management_restaurantimage`
--
ALTER TABLE `user_management_restaurantimage`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_management_rest_restaurant_id_3d0ef107_fk_user_mana` (`restaurant_id`);

--
-- Indici per le tabelle `user_management_restaurant_kitchen_types`
--
ALTER TABLE `user_management_restaurant_kitchen_types`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_management_restaura_restaurant_id_kitchentyp_227875a7_uniq` (`restaurant_id`,`kitchentype_id`),
  ADD KEY `user_management_rest_kitchentype_id_77369e28_fk_user_mana` (`kitchentype_id`);

--
-- Indici per le tabelle `user_management_restaurant_services`
--
ALTER TABLE `user_management_restaurant_services`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_management_restaura_restaurant_id_service_id_a1d4ba8b_uniq` (`restaurant_id`,`service_id`),
  ADD KEY `user_management_rest_service_id_9eeeff36_fk_user_mana` (`service_id`);

--
-- Indici per le tabelle `user_management_service`
--
ALTER TABLE `user_management_service`
  ADD PRIMARY KEY (`id`);

--
-- Indici per le tabelle `user_management_user`
--
ALTER TABLE `user_management_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `restaurant_information_id` (`restaurant_information_id`);

--
-- Indici per le tabelle `user_management_user_groups`
--
ALTER TABLE `user_management_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_management_user_groups_user_id_group_id_bed1779a_uniq` (`user_id`,`group_id`),
  ADD KEY `user_management_user_groups_group_id_6f577055_fk_auth_group_id` (`group_id`);

--
-- Indici per le tabelle `user_management_user_user_permissions`
--
ALTER TABLE `user_management_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_management_user_use_user_id_permission_id_c71a3268_uniq` (`user_id`,`permission_id`),
  ADD KEY `user_management_user_permission_id_d8c2b1e9_fk_auth_perm` (`permission_id`);

--
-- AUTO_INCREMENT per le tabelle scaricate
--

--
-- AUTO_INCREMENT per la tabella `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT per la tabella `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT per la tabella `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=40;
--
-- AUTO_INCREMENT per la tabella `booking_booking`
--
ALTER TABLE `booking_booking`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT per la tabella `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
--
-- AUTO_INCREMENT per la tabella `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT per la tabella `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
--
-- AUTO_INCREMENT per la tabella `user_management_kitchentype`
--
ALTER TABLE `user_management_kitchentype`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT per la tabella `user_management_menucategory`
--
ALTER TABLE `user_management_menucategory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT per la tabella `user_management_menuvoice`
--
ALTER TABLE `user_management_menuvoice`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT per la tabella `user_management_restaurant`
--
ALTER TABLE `user_management_restaurant`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT per la tabella `user_management_restaurantimage`
--
ALTER TABLE `user_management_restaurantimage`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT per la tabella `user_management_restaurant_kitchen_types`
--
ALTER TABLE `user_management_restaurant_kitchen_types`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT per la tabella `user_management_restaurant_services`
--
ALTER TABLE `user_management_restaurant_services`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT per la tabella `user_management_service`
--
ALTER TABLE `user_management_service`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT per la tabella `user_management_user`
--
ALTER TABLE `user_management_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
--
-- AUTO_INCREMENT per la tabella `user_management_user_groups`
--
ALTER TABLE `user_management_user_groups`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT per la tabella `user_management_user_user_permissions`
--
ALTER TABLE `user_management_user_user_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- Limiti per le tabelle scaricate
--

--
-- Limiti per la tabella `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Limiti per la tabella `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Limiti per la tabella `booking_booking`
--
ALTER TABLE `booking_booking`
  ADD CONSTRAINT `booking_booking_client_id_4b0e9d36_fk_user_management_user_id` FOREIGN KEY (`client_id`) REFERENCES `user_management_user` (`id`),
  ADD CONSTRAINT `booking_booking_restaurant_id_4188bc98_fk_user_mana` FOREIGN KEY (`restaurant_id`) REFERENCES `user_management_restaurant` (`id`);

--
-- Limiti per la tabella `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_user_management_user_id` FOREIGN KEY (`user_id`) REFERENCES `user_management_user` (`id`);

--
-- Limiti per la tabella `user_management_menucategory`
--
ALTER TABLE `user_management_menucategory`
  ADD CONSTRAINT `user_management_menu_restaurant_id_30692d9d_fk_user_mana` FOREIGN KEY (`restaurant_id`) REFERENCES `user_management_restaurant` (`id`);

--
-- Limiti per la tabella `user_management_menuvoice`
--
ALTER TABLE `user_management_menuvoice`
  ADD CONSTRAINT `user_management_menu_menu_category_id_109e7e45_fk_user_mana` FOREIGN KEY (`menu_category_id`) REFERENCES `user_management_menucategory` (`id`);

--
-- Limiti per la tabella `user_management_restaurantimage`
--
ALTER TABLE `user_management_restaurantimage`
  ADD CONSTRAINT `user_management_rest_restaurant_id_3d0ef107_fk_user_mana` FOREIGN KEY (`restaurant_id`) REFERENCES `user_management_restaurant` (`id`);

--
-- Limiti per la tabella `user_management_restaurant_kitchen_types`
--
ALTER TABLE `user_management_restaurant_kitchen_types`
  ADD CONSTRAINT `user_management_rest_kitchentype_id_77369e28_fk_user_mana` FOREIGN KEY (`kitchentype_id`) REFERENCES `user_management_kitchentype` (`id`),
  ADD CONSTRAINT `user_management_rest_restaurant_id_d2dcc3f9_fk_user_mana` FOREIGN KEY (`restaurant_id`) REFERENCES `user_management_restaurant` (`id`);

--
-- Limiti per la tabella `user_management_restaurant_services`
--
ALTER TABLE `user_management_restaurant_services`
  ADD CONSTRAINT `user_management_rest_restaurant_id_746d6dd8_fk_user_mana` FOREIGN KEY (`restaurant_id`) REFERENCES `user_management_restaurant` (`id`),
  ADD CONSTRAINT `user_management_rest_service_id_9eeeff36_fk_user_mana` FOREIGN KEY (`service_id`) REFERENCES `user_management_service` (`id`);

--
-- Limiti per la tabella `user_management_user`
--
ALTER TABLE `user_management_user`
  ADD CONSTRAINT `user_management_user_restaurant_informati_9d2552b3_fk_user_mana` FOREIGN KEY (`restaurant_information_id`) REFERENCES `user_management_restaurant` (`id`);

--
-- Limiti per la tabella `user_management_user_groups`
--
ALTER TABLE `user_management_user_groups`
  ADD CONSTRAINT `user_management_user_groups_group_id_6f577055_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `user_management_user_user_id_092e6f6b_fk_user_mana` FOREIGN KEY (`user_id`) REFERENCES `user_management_user` (`id`);

--
-- Limiti per la tabella `user_management_user_user_permissions`
--
ALTER TABLE `user_management_user_user_permissions`
  ADD CONSTRAINT `user_management_user_permission_id_d8c2b1e9_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `user_management_user_user_id_4b8c2c7b_fk_user_mana` FOREIGN KEY (`user_id`) REFERENCES `user_management_user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
