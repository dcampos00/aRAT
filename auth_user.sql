-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 05, 2013 at 01:30 PM
-- Server version: 5.5.29
-- PHP Version: 5.4.6-1ubuntu1.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `arat_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=31 ;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add permission', 1, 'add_permission'),
(2, 'Can change permission', 1, 'change_permission'),
(3, 'Can delete permission', 1, 'delete_permission'),
(4, 'Can add group', 2, 'add_group'),
(5, 'Can change group', 2, 'change_group'),
(6, 'Can delete group', 2, 'delete_group'),
(7, 'Can add user', 3, 'add_user'),
(8, 'Can change user', 3, 'change_user'),
(9, 'Can delete user', 3, 'delete_user'),
(10, 'Can add content type', 4, 'add_contenttype'),
(11, 'Can change content type', 4, 'change_contenttype'),
(12, 'Can delete content type', 4, 'delete_contenttype'),
(13, 'Can add session', 5, 'add_session'),
(14, 'Can change session', 5, 'change_session'),
(15, 'Can delete session', 5, 'delete_session'),
(16, 'Can add site', 6, 'add_site'),
(17, 'Can change site', 6, 'change_site'),
(18, 'Can delete site', 6, 'delete_site'),
(19, 'Can add log entry', 7, 'add_logentry'),
(20, 'Can change log entry', 7, 'change_logentry'),
(21, 'Can delete log entry', 7, 'delete_logentry'),
(22, 'Can add antenna', 8, 'add_antenna'),
(23, 'Can change antenna', 8, 'change_antenna'),
(24, 'Can delete antenna', 8, 'delete_antenna'),
(25, 'Can add settings', 9, 'add_settings'),
(26, 'Can change settings', 9, 'change_settings'),
(27, 'Can delete settings', 9, 'delete_settings'),
(28, 'Can add pad', 10, 'add_pad'),
(29, 'Can change pad', 10, 'change_pad'),
(30, 'Can delete pad', 10, 'delete_pad');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`) VALUES
(1, 'admin', '', '', 'dcampos00@gmail.com', 'pbkdf2_sha256$10000$GBhDx1GFXKs3$Cqxo3rB8md0j5N2Z//LO3pUUUmngaHYBnopkxoUF9+w=', 1, 1, 1, '2013-02-04 19:40:12', '2013-02-01 18:42:50'),
(2, 'dcampos', 'Daniel', 'Campos', 'dcampos00@gmail.com', '!', 0, 1, 0, '2013-02-04 13:02:42', '2013-02-01 18:58:57');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `common_settings`
--

DROP TABLE IF EXISTS `common_settings`;
CREATE TABLE IF NOT EXISTS `common_settings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `setting` varchar(5) NOT NULL,
  `value` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `setting` (`setting`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `common_settings`
--

INSERT INTO `common_settings` (`id`, `setting`, `value`) VALUES
(1, 'BLOCK', 0);

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10 ;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `user_id`, `content_type_id`, `object_id`, `object_repr`, `action_flag`, `change_message`) VALUES
(1, '2013-02-01 19:14:21', 1, 8, '1', 'DV01', 2, 'Changed current_ste.'),
(2, '2013-02-01 19:15:12', 1, 8, '1', 'DV01', 2, 'Changed current_ste.'),
(3, '2013-02-04 19:40:39', 1, 8, '1', 'DV01', 2, 'Changed current_pad.'),
(4, '2013-02-04 20:26:10', 1, 8, '65', 'CM12', 2, 'Changed current_pad.'),
(5, '2013-02-04 20:41:06', 1, 8, '49', 'DA65', 2, 'Changed current_pad.'),
(6, '2013-02-04 20:41:30', 1, 8, '9', 'DV09', 2, 'Changed current_pad.'),
(7, '2013-02-04 21:13:46', 1, 10, '202', 'PAD object', 2, 'Changed current_antenna.'),
(8, '2013-02-04 21:23:57', 1, 10, '199', 'PAD TF07', 2, 'Changed current_antenna.'),
(9, '2013-02-05 13:22:43', 1, 10, '4', 'PAD T701', 2, 'Changed current_antenna.');

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=11 ;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES
(1, 'permission', 'auth', 'permission'),
(2, 'group', 'auth', 'group'),
(3, 'user', 'auth', 'user'),
(4, 'content type', 'contenttypes', 'contenttype'),
(5, 'session', 'sessions', 'session'),
(6, 'site', 'sites', 'site'),
(7, 'log entry', 'admin', 'logentry'),
(8, 'antenna', 'home', 'antenna'),
(9, 'settings', 'common', 'settings'),
(10, 'pad', 'home', 'pad');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('45fd474486feffd9b67048c77e5a435c', 'NDU2MTlmZjcyNTE3YWJkODgxYzk4OTc1MWI3Y2U5NDJkOWQyOTRhZjqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n', '2013-02-18 19:40:12');

-- --------------------------------------------------------

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
CREATE TABLE IF NOT EXISTS `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `django_site`
--

INSERT INTO `django_site` (`id`, `domain`, `name`) VALUES
(1, 'example.com', 'example.com');

-- --------------------------------------------------------

--
-- Table structure for table `home_antenna`
--

DROP TABLE IF EXISTS `home_antenna`;
CREATE TABLE IF NOT EXISTS `home_antenna` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(5) NOT NULL,
  `current_ste` int(11) DEFAULT NULL,
  `requested_ste` int(11) DEFAULT NULL,
  `requester_id` int(11) DEFAULT NULL,
  `request_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `home_antenna_b8ca8b9f` (`requester_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=66 ;

--
-- Dumping data for table `home_antenna`
--

INSERT INTO `home_antenna` (`id`, `name`, `current_ste`, `requested_ste`, `requester_id`, `request_date`) VALUES
(1, 'DV01', 5, NULL, NULL, NULL),
(2, 'DV02', 5, NULL, NULL, NULL),
(3, 'DV03', 5, NULL, NULL, NULL),
(4, 'DV04', 5, NULL, NULL, NULL),
(5, 'DV05', 5, NULL, NULL, NULL),
(6, 'DV06', 5, NULL, NULL, NULL),
(7, 'DV07', 5, NULL, NULL, NULL),
(8, 'DV08', 5, NULL, NULL, NULL),
(9, 'DV09', 5, NULL, NULL, NULL),
(10, 'DV10', 5, NULL, NULL, NULL),
(11, 'DV12', 5, NULL, NULL, NULL),
(12, 'DV13', 5, NULL, NULL, NULL),
(13, 'DV14', 5, NULL, NULL, NULL),
(14, 'DV15', 5, NULL, NULL, NULL),
(15, 'DV16', 5, NULL, NULL, NULL),
(16, 'DV17', 5, NULL, NULL, NULL),
(17, 'DV18', 5, NULL, NULL, NULL),
(18, 'DV19', 5, NULL, NULL, NULL),
(19, 'DV20', 5, NULL, NULL, NULL),
(20, 'DV21', 5, NULL, NULL, NULL),
(21, 'DV22', 5, NULL, NULL, NULL),
(22, 'DV23', 5, NULL, NULL, NULL),
(23, 'DV24', 5, NULL, NULL, NULL),
(24, 'DV25', 5, NULL, NULL, NULL),
(25, 'DA41', 5, NULL, NULL, NULL),
(26, 'DA42', 5, NULL, NULL, NULL),
(27, 'DA43', 5, NULL, NULL, NULL),
(28, 'DA44', 5, NULL, NULL, NULL),
(29, 'DA45', 5, NULL, NULL, NULL),
(30, 'DA46', 5, NULL, NULL, NULL),
(31, 'DA47', 5, NULL, NULL, NULL),
(32, 'DA48', 5, NULL, NULL, NULL),
(33, 'DA49', 5, NULL, NULL, NULL),
(34, 'DA50', 5, NULL, NULL, NULL),
(35, 'DA51', 5, NULL, NULL, NULL),
(36, 'DA52', 5, NULL, NULL, NULL),
(37, 'DA53', 5, NULL, NULL, NULL),
(38, 'DA54', 5, NULL, NULL, NULL),
(39, 'DA55', 5, NULL, NULL, NULL),
(40, 'DA56', 5, NULL, NULL, NULL),
(41, 'DA57', 5, NULL, NULL, NULL),
(42, 'DA58', 5, NULL, NULL, NULL),
(43, 'DA59', 5, NULL, NULL, NULL),
(44, 'DA60', 5, NULL, NULL, NULL),
(45, 'DA61', 5, NULL, NULL, NULL),
(46, 'DA62', 5, NULL, NULL, NULL),
(47, 'DA63', 5, NULL, NULL, NULL),
(48, 'DA64', 5, NULL, NULL, NULL),
(49, 'DA65', 5, NULL, NULL, NULL),
(50, 'PM01', 5, NULL, NULL, NULL),
(51, 'PM02', 5, NULL, NULL, NULL),
(52, 'PM03', 5, NULL, NULL, NULL),
(53, 'PM04', 5, NULL, NULL, NULL),
(54, 'CM01', 5, NULL, NULL, NULL),
(55, 'CM02', 5, NULL, NULL, NULL),
(56, 'CM03', 5, NULL, NULL, NULL),
(57, 'CM04', 5, NULL, NULL, NULL),
(58, 'CM05', 5, NULL, NULL, NULL),
(59, 'CM06', 5, NULL, NULL, NULL),
(60, 'CM07', 5, NULL, NULL, NULL),
(61, 'CM08', 5, NULL, NULL, NULL),
(62, 'CM09', 5, NULL, NULL, NULL),
(63, 'CM10', 5, NULL, NULL, NULL),
(64, 'CM11', 5, NULL, NULL, NULL),
(65, 'CM12', 5, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `home_pad`
--

DROP TABLE IF EXISTS `home_pad`;
CREATE TABLE IF NOT EXISTS `home_pad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(5) NOT NULL,
  `current_antenna_id` int(11) DEFAULT NULL,
  `requested_antenna_id` int(11) DEFAULT NULL,
  `requester_id` int(11) DEFAULT NULL,
  `request_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `current_antenna_id` (`current_antenna_id`),
  KEY `home_pad_62753b47` (`requested_antenna_id`),
  KEY `home_pad_b8ca8b9f` (`requester_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=203 ;

--
-- Dumping data for table `home_pad`
--

INSERT INTO `home_pad` (`id`, `name`, `current_antenna_id`, `requested_antenna_id`, `requester_id`, `request_date`) VALUES
(1, 'T703', NULL, NULL, NULL, NULL),
(2, 'T702', NULL, NULL, NULL, NULL),
(3, 'T704', NULL, NULL, NULL, NULL),
(4, 'T701', 1, NULL, NULL, NULL),
(5, 'A007', NULL, NULL, NULL, NULL),
(6, 'A011', NULL, NULL, NULL, NULL),
(7, 'A015', NULL, NULL, NULL, NULL),
(8, 'A020', NULL, NULL, NULL, NULL),
(9, 'A008', NULL, NULL, NULL, NULL),
(10, 'A080', NULL, NULL, NULL, NULL),
(11, 'A138', NULL, NULL, NULL, NULL),
(12, 'A069', NULL, NULL, NULL, NULL),
(13, 'A074', NULL, NULL, NULL, NULL),
(14, 'A025', NULL, NULL, NULL, NULL),
(15, 'A072', NULL, NULL, NULL, NULL),
(16, 'A031', NULL, NULL, NULL, NULL),
(17, 'A071', NULL, 7, NULL, NULL),
(18, 'A021', NULL, NULL, NULL, NULL),
(19, 'A006', NULL, NULL, NULL, NULL),
(20, 'A037', NULL, NULL, NULL, NULL),
(21, 'A082', NULL, NULL, NULL, NULL),
(22, 'A004', NULL, NULL, NULL, NULL),
(23, 'A137', NULL, NULL, NULL, NULL),
(24, 'A077', NULL, NULL, NULL, NULL),
(25, 'A001', NULL, NULL, NULL, NULL),
(26, 'A054', NULL, NULL, NULL, NULL),
(27, 'A063', NULL, NULL, NULL, NULL),
(28, 'A038', NULL, NULL, NULL, NULL),
(29, 'A035', NULL, NULL, NULL, NULL),
(30, 'A017', NULL, NULL, NULL, NULL),
(31, 'A045', NULL, NULL, NULL, NULL),
(32, 'A029', NULL, NULL, NULL, NULL),
(33, 'A046', NULL, NULL, NULL, NULL),
(34, 'A026', NULL, NULL, NULL, NULL),
(35, 'A067', NULL, NULL, NULL, NULL),
(36, 'A070', NULL, NULL, NULL, NULL),
(37, 'A068', NULL, NULL, NULL, NULL),
(38, 'A075', NULL, NULL, NULL, NULL),
(39, 'A050', NULL, NULL, NULL, NULL),
(40, 'A003', NULL, NULL, NULL, NULL),
(41, 'J504', NULL, NULL, NULL, NULL),
(42, 'J501', NULL, NULL, NULL, NULL),
(43, 'J509', NULL, NULL, NULL, NULL),
(44, 'J505', NULL, NULL, NULL, NULL),
(45, 'J507', NULL, NULL, NULL, NULL),
(46, 'J512', NULL, NULL, NULL, NULL),
(47, 'J506', NULL, NULL, NULL, NULL),
(48, 'J511', NULL, NULL, NULL, NULL),
(49, 'J503', NULL, NULL, NULL, NULL),
(50, 'J502', NULL, NULL, NULL, NULL),
(51, 'J508', NULL, NULL, NULL, NULL),
(52, 'A002', NULL, NULL, NULL, NULL),
(53, 'A005', NULL, NULL, NULL, NULL),
(54, 'A009', NULL, NULL, NULL, NULL),
(55, 'A010', NULL, NULL, NULL, NULL),
(56, 'A012', NULL, NULL, NULL, NULL),
(57, 'A013', NULL, NULL, NULL, NULL),
(58, 'A014', NULL, NULL, NULL, NULL),
(59, 'A016', NULL, NULL, NULL, NULL),
(60, 'A018', NULL, NULL, NULL, NULL),
(61, 'A019', NULL, NULL, NULL, NULL),
(62, 'A022', NULL, NULL, NULL, NULL),
(63, 'A023', NULL, NULL, NULL, NULL),
(64, 'A024', NULL, NULL, NULL, NULL),
(65, 'A027', NULL, NULL, NULL, NULL),
(66, 'A028', NULL, NULL, NULL, NULL),
(67, 'A030', NULL, NULL, NULL, NULL),
(68, 'A032', NULL, NULL, NULL, NULL),
(69, 'A033', NULL, NULL, NULL, NULL),
(70, 'A034', NULL, 8, NULL, NULL),
(71, 'A036', NULL, NULL, NULL, NULL),
(72, 'A039', NULL, NULL, NULL, NULL),
(73, 'A040', NULL, NULL, NULL, NULL),
(74, 'A041', NULL, NULL, NULL, NULL),
(75, 'A042', NULL, NULL, NULL, NULL),
(76, 'A043', NULL, NULL, NULL, NULL),
(77, 'A044', NULL, NULL, NULL, NULL),
(78, 'A047', NULL, NULL, NULL, NULL),
(79, 'A048', NULL, NULL, NULL, NULL),
(80, 'A049', NULL, NULL, NULL, NULL),
(81, 'A051', NULL, NULL, NULL, NULL),
(82, 'A052', NULL, NULL, NULL, NULL),
(83, 'A053', NULL, NULL, NULL, NULL),
(84, 'A055', NULL, NULL, NULL, NULL),
(85, 'A056', NULL, NULL, NULL, NULL),
(86, 'A057', NULL, NULL, NULL, NULL),
(87, 'A058', NULL, NULL, NULL, NULL),
(88, 'A059', NULL, NULL, NULL, NULL),
(89, 'A060', NULL, NULL, NULL, NULL),
(90, 'A061', NULL, NULL, NULL, NULL),
(91, 'A062', NULL, NULL, NULL, NULL),
(92, 'A064', NULL, NULL, NULL, NULL),
(93, 'A065', NULL, NULL, NULL, NULL),
(94, 'A066', NULL, NULL, NULL, NULL),
(95, 'A073', NULL, NULL, NULL, NULL),
(96, 'A076', NULL, NULL, NULL, NULL),
(97, 'A078', NULL, NULL, NULL, NULL),
(98, 'A079', NULL, NULL, NULL, NULL),
(99, 'A081', NULL, NULL, NULL, NULL),
(100, 'A083', NULL, NULL, NULL, NULL),
(101, 'A084', NULL, NULL, NULL, NULL),
(102, 'A085', NULL, NULL, NULL, NULL),
(103, 'A086', NULL, NULL, NULL, NULL),
(104, 'A087', NULL, NULL, NULL, NULL),
(105, 'A088', NULL, NULL, NULL, NULL),
(106, 'A089', NULL, NULL, NULL, NULL),
(107, 'A090', NULL, NULL, NULL, NULL),
(108, 'A091', NULL, NULL, NULL, NULL),
(109, 'A092', NULL, NULL, NULL, NULL),
(110, 'A093', NULL, NULL, NULL, NULL),
(111, 'A094', NULL, NULL, NULL, NULL),
(112, 'A095', NULL, NULL, NULL, NULL),
(113, 'A096', NULL, NULL, NULL, NULL),
(114, 'A097', NULL, NULL, NULL, NULL),
(115, 'A098', NULL, NULL, NULL, NULL),
(116, 'A099', NULL, NULL, NULL, NULL),
(117, 'A100', NULL, NULL, NULL, NULL),
(118, 'A101', NULL, NULL, NULL, NULL),
(119, 'A102', NULL, NULL, NULL, NULL),
(120, 'A103', NULL, NULL, NULL, NULL),
(121, 'A104', NULL, NULL, NULL, NULL),
(122, 'A105', NULL, NULL, NULL, NULL),
(123, 'A106', NULL, NULL, NULL, NULL),
(124, 'A107', NULL, NULL, NULL, NULL),
(125, 'A108', NULL, NULL, NULL, NULL),
(126, 'A109', NULL, NULL, NULL, NULL),
(127, 'A110', NULL, NULL, NULL, NULL),
(128, 'A111', NULL, NULL, NULL, NULL),
(129, 'A112', NULL, NULL, NULL, NULL),
(130, 'A113', NULL, NULL, NULL, NULL),
(131, 'A114', NULL, NULL, NULL, NULL),
(132, 'A115', NULL, NULL, NULL, NULL),
(133, 'A116', NULL, NULL, NULL, NULL),
(134, 'A117', NULL, NULL, NULL, NULL),
(135, 'A118', NULL, NULL, NULL, NULL),
(136, 'A119', NULL, NULL, NULL, NULL),
(137, 'A120', NULL, NULL, NULL, NULL),
(138, 'A121', NULL, NULL, NULL, NULL),
(139, 'A122', NULL, NULL, NULL, NULL),
(140, 'A123', NULL, NULL, NULL, NULL),
(141, 'A124', NULL, NULL, NULL, NULL),
(142, 'A125', NULL, NULL, NULL, NULL),
(143, 'A126', NULL, NULL, NULL, NULL),
(144, 'A127', NULL, NULL, NULL, NULL),
(145, 'A128', NULL, NULL, NULL, NULL),
(146, 'A129', NULL, NULL, NULL, NULL),
(147, 'A130', NULL, NULL, NULL, NULL),
(148, 'A131', NULL, NULL, NULL, NULL),
(149, 'A132', NULL, NULL, NULL, NULL),
(150, 'A133', NULL, NULL, NULL, NULL),
(151, 'A134', NULL, NULL, NULL, NULL),
(152, 'A135', NULL, NULL, NULL, NULL),
(153, 'A136', NULL, NULL, NULL, NULL),
(154, 'J510', NULL, NULL, NULL, NULL),
(155, 'N601', NULL, NULL, NULL, NULL),
(156, 'N602', NULL, NULL, NULL, NULL),
(157, 'N603', NULL, NULL, NULL, NULL),
(158, 'N604', NULL, NULL, NULL, NULL),
(159, 'N605', NULL, NULL, NULL, NULL),
(160, 'N606', NULL, NULL, NULL, NULL),
(161, 'P401', NULL, NULL, NULL, NULL),
(162, 'P402', NULL, NULL, NULL, NULL),
(163, 'P403', NULL, NULL, NULL, NULL),
(164, 'P404', NULL, NULL, NULL, NULL),
(165, 'P405', NULL, NULL, NULL, NULL),
(166, 'P406', NULL, NULL, NULL, NULL),
(167, 'P407', NULL, NULL, NULL, NULL),
(168, 'P408', NULL, NULL, NULL, NULL),
(169, 'P409', NULL, NULL, NULL, NULL),
(170, 'P410', NULL, NULL, NULL, NULL),
(171, 'P411', NULL, NULL, NULL, NULL),
(172, 'P412', NULL, NULL, NULL, NULL),
(173, 'P413', NULL, NULL, NULL, NULL),
(174, 'S301', NULL, NULL, NULL, NULL),
(175, 'S302', NULL, NULL, NULL, NULL),
(176, 'S303', NULL, NULL, NULL, NULL),
(177, 'S304', NULL, NULL, NULL, NULL),
(178, 'S305', NULL, NULL, NULL, NULL),
(179, 'S306', NULL, NULL, NULL, NULL),
(180, 'S307', NULL, NULL, NULL, NULL),
(181, 'S308', NULL, NULL, NULL, NULL),
(182, 'S309', NULL, NULL, NULL, NULL),
(183, 'W201', NULL, NULL, NULL, NULL),
(184, 'W202', NULL, NULL, NULL, NULL),
(185, 'W203', NULL, NULL, NULL, NULL),
(186, 'W204', NULL, NULL, NULL, NULL),
(187, 'W205', NULL, NULL, NULL, NULL),
(188, 'W206', NULL, NULL, NULL, NULL),
(189, 'W207', NULL, NULL, NULL, NULL),
(190, 'W208', NULL, NULL, NULL, NULL),
(191, 'W209', NULL, NULL, NULL, NULL),
(192, 'W210', NULL, NULL, NULL, NULL),
(193, 'TF01', NULL, NULL, NULL, NULL),
(194, 'TF02', NULL, 7, NULL, NULL),
(195, 'TF03', NULL, NULL, NULL, NULL),
(196, 'TF04', NULL, NULL, NULL, NULL),
(197, 'TF05', NULL, 11, NULL, NULL),
(198, 'TF06', NULL, 2, NULL, NULL),
(199, 'TF07', NULL, NULL, NULL, NULL),
(200, 'TF08', NULL, 2, NULL, NULL),
(201, 'TF09', NULL, NULL, NULL, NULL),
(202, 'TF10', NULL, NULL, NULL, NULL);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `home_antenna`
--
ALTER TABLE `home_antenna`
  ADD CONSTRAINT `requester_id_refs_id_aa61ccb1` FOREIGN KEY (`requester_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `home_pad`
--
ALTER TABLE `home_pad`
  ADD CONSTRAINT `requested_antenna_id_refs_id_f8b00e53` FOREIGN KEY (`requested_antenna_id`) REFERENCES `home_antenna` (`id`),
  ADD CONSTRAINT `current_antenna_id_refs_id_f8b00e53` FOREIGN KEY (`current_antenna_id`) REFERENCES `home_antenna` (`id`),
  ADD CONSTRAINT `requester_id_refs_id_24362f31` FOREIGN KEY (`requester_id`) REFERENCES `auth_user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
