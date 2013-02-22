-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 22, 2013 at 10:54 AM
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

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=46 ;

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
(16, 'Can add log entry', 6, 'add_logentry'),
(17, 'Can change log entry', 6, 'change_logentry'),
(18, 'Can delete log entry', 6, 'delete_logentry'),
(19, 'Can add configuration', 7, 'add_configuration'),
(20, 'Can change configuration', 7, 'change_configuration'),
(21, 'Can delete configuration', 7, 'delete_configuration'),
(22, 'Can add history', 8, 'add_history'),
(23, 'Can change history', 8, 'change_history'),
(24, 'Can delete history', 8, 'delete_history'),
(25, 'Can add table header', 9, 'add_tableheader'),
(26, 'Can change table header', 9, 'change_tableheader'),
(27, 'Can delete table header', 9, 'delete_tableheader'),
(28, 'Can add resource', 10, 'add_resource'),
(29, 'Can change resource', 10, 'change_resource'),
(30, 'Can delete resource', 10, 'delete_resource'),
(31, 'Can add antenna', 11, 'add_antenna'),
(32, 'Can change antenna', 11, 'change_antenna'),
(33, 'Can delete antenna', 11, 'delete_antenna'),
(34, 'Can add pad', 12, 'add_pad'),
(35, 'Can change pad', 12, 'change_pad'),
(36, 'Can delete pad', 12, 'delete_pad'),
(37, 'Can add correlator configuration', 13, 'add_correlatorconfiguration'),
(38, 'Can change correlator configuration', 13, 'change_correlatorconfiguration'),
(39, 'Can delete correlator configuration', 13, 'delete_correlatorconfiguration'),
(40, 'Can add centrallo configuration', 14, 'add_centralloconfiguration'),
(41, 'Can change centrallo configuration', 14, 'change_centralloconfiguration'),
(42, 'Can delete centrallo configuration', 14, 'delete_centralloconfiguration'),
(43, 'Can add holography configuration', 15, 'add_holographyconfiguration'),
(44, 'Can change holography configuration', 15, 'change_holographyconfiguration'),
(45, 'Can delete holography configuration', 15, 'delete_holographyconfiguration');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `username`, `first_name`, `last_name`, `email`, `password`, `is_staff`, `is_active`, `is_superuser`, `last_login`, `date_joined`) VALUES
(1, 'admin', '', '', 'dcampos00@gmail.com', 'pbkdf2_sha256$10000$8f2KATkvXmTx$X0KUjBsQxQEC5TZnTtmh27OjfLLhkjQaZCSAW0bwHBA=', 1, 1, 1, '2013-02-22 13:54:09', '2013-02-22 13:54:09');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

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
-- Table structure for table `common_configuration`
--

CREATE TABLE IF NOT EXISTS `common_configuration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `setting` varchar(5) NOT NULL,
  `value` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `setting` (`setting`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

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
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=16 ;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `name`, `app_label`, `model`) VALUES
(1, 'permission', 'auth', 'permission'),
(2, 'group', 'auth', 'group'),
(3, 'user', 'auth', 'user'),
(4, 'content type', 'contenttypes', 'contenttype'),
(5, 'session', 'sessions', 'session'),
(6, 'log entry', 'admin', 'logentry'),
(7, 'configuration', 'common', 'configuration'),
(8, 'history', 'home', 'history'),
(9, 'table header', 'home', 'tableheader'),
(10, 'resource', 'home', 'resource'),
(11, 'antenna', 'home', 'antenna'),
(12, 'pad', 'home', 'pad'),
(13, 'correlator configuration', 'home', 'correlatorconfiguration'),
(14, 'centrallo configuration', 'home', 'centralloconfiguration'),
(15, 'holography configuration', 'home', 'holographyconfiguration');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `home_antenna`
--

CREATE TABLE IF NOT EXISTS `home_antenna` (
  `resource_ptr_id` int(11) NOT NULL,
  `name` varchar(5) NOT NULL,
  `current_ste` varchar(10) DEFAULT NULL,
  `requested_ste` varchar(10) DEFAULT NULL,
  `current_band` varchar(100) NOT NULL,
  `requested_band` varchar(100) NOT NULL,
  `vendor` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`resource_ptr_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `home_centralloconfiguration`
--

CREATE TABLE IF NOT EXISTS `home_centralloconfiguration` (
  `resource_ptr_id` int(11) NOT NULL,
  `identifier` varchar(20) NOT NULL,
  `configuration` longtext NOT NULL,
  `centrallo` varchar(10) NOT NULL,
  `assigned` tinyint(1) NOT NULL,
  `header_id` int(11) NOT NULL,
  `current_antenna_id` int(11) DEFAULT NULL,
  `requested_antenna_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`resource_ptr_id`),
  KEY `home_centralloconfiguration_7918d61b` (`header_id`),
  KEY `home_centralloconfiguration_38f06868` (`current_antenna_id`),
  KEY `home_centralloconfiguration_62753b47` (`requested_antenna_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `home_correlatorconfiguration`
--

CREATE TABLE IF NOT EXISTS `home_correlatorconfiguration` (
  `resource_ptr_id` int(11) NOT NULL,
  `caimap` int(11) NOT NULL,
  `configuration` longtext NOT NULL,
  `correlator` varchar(10) NOT NULL,
  `assigned` tinyint(1) NOT NULL,
  `header_id` int(11) NOT NULL,
  `current_antenna_id` int(11) DEFAULT NULL,
  `requested_antenna_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`resource_ptr_id`),
  KEY `home_correlatorconfiguration_7918d61b` (`header_id`),
  KEY `home_correlatorconfiguration_38f06868` (`current_antenna_id`),
  KEY `home_correlatorconfiguration_62753b47` (`requested_antenna_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `home_history`
--

CREATE TABLE IF NOT EXISTS `home_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_time` datetime NOT NULL,
  `request` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `home_holographyconfiguration`
--

CREATE TABLE IF NOT EXISTS `home_holographyconfiguration` (
  `resource_ptr_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `assigned` tinyint(1) NOT NULL,
  `current_antenna_id` int(11) DEFAULT NULL,
  `requested_antenna_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`resource_ptr_id`),
  KEY `home_holographyconfiguration_38f06868` (`current_antenna_id`),
  KEY `home_holographyconfiguration_62753b47` (`requested_antenna_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `home_pad`
--

CREATE TABLE IF NOT EXISTS `home_pad` (
  `resource_ptr_id` int(11) NOT NULL,
  `location` varchar(10) NOT NULL,
  `name` varchar(10) NOT NULL,
  `assigned` tinyint(1) NOT NULL,
  `current_antenna_id` int(11) DEFAULT NULL,
  `requested_antenna_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`resource_ptr_id`),
  UNIQUE KEY `name` (`name`),
  KEY `home_pad_38f06868` (`current_antenna_id`),
  KEY `home_pad_62753b47` (`requested_antenna_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `home_resource`
--

CREATE TABLE IF NOT EXISTS `home_resource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) NOT NULL,
  `requester_id` int(11) DEFAULT NULL,
  `request_date` datetime DEFAULT NULL,
  `errors` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `home_resource_b8ca8b9f` (`requester_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `home_tableheader`
--

CREATE TABLE IF NOT EXISTS `home_tableheader` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` longtext NOT NULL,
  `resource` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `resource` (`resource`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

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
  ADD CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

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
  ADD CONSTRAINT `resource_ptr_id_refs_id_f8c61861` FOREIGN KEY (`resource_ptr_id`) REFERENCES `home_resource` (`id`);

--
-- Constraints for table `home_centralloconfiguration`
--
ALTER TABLE `home_centralloconfiguration`
  ADD CONSTRAINT `requested_antenna_id_refs_resource_ptr_id_41754efb` FOREIGN KEY (`requested_antenna_id`) REFERENCES `home_antenna` (`resource_ptr_id`),
  ADD CONSTRAINT `current_antenna_id_refs_resource_ptr_id_41754efb` FOREIGN KEY (`current_antenna_id`) REFERENCES `home_antenna` (`resource_ptr_id`),
  ADD CONSTRAINT `header_id_refs_id_f7792ecf` FOREIGN KEY (`header_id`) REFERENCES `home_tableheader` (`id`),
  ADD CONSTRAINT `resource_ptr_id_refs_id_ca91c3bf` FOREIGN KEY (`resource_ptr_id`) REFERENCES `home_resource` (`id`);

--
-- Constraints for table `home_correlatorconfiguration`
--
ALTER TABLE `home_correlatorconfiguration`
  ADD CONSTRAINT `requested_antenna_id_refs_resource_ptr_id_ae9034c7` FOREIGN KEY (`requested_antenna_id`) REFERENCES `home_antenna` (`resource_ptr_id`),
  ADD CONSTRAINT `current_antenna_id_refs_resource_ptr_id_ae9034c7` FOREIGN KEY (`current_antenna_id`) REFERENCES `home_antenna` (`resource_ptr_id`),
  ADD CONSTRAINT `header_id_refs_id_d91d6b65` FOREIGN KEY (`header_id`) REFERENCES `home_tableheader` (`id`),
  ADD CONSTRAINT `resource_ptr_id_refs_id_c4a870f3` FOREIGN KEY (`resource_ptr_id`) REFERENCES `home_resource` (`id`);

--
-- Constraints for table `home_holographyconfiguration`
--
ALTER TABLE `home_holographyconfiguration`
  ADD CONSTRAINT `requested_antenna_id_refs_resource_ptr_id_65ef957b` FOREIGN KEY (`requested_antenna_id`) REFERENCES `home_antenna` (`resource_ptr_id`),
  ADD CONSTRAINT `current_antenna_id_refs_resource_ptr_id_65ef957b` FOREIGN KEY (`current_antenna_id`) REFERENCES `home_antenna` (`resource_ptr_id`),
  ADD CONSTRAINT `resource_ptr_id_refs_id_b332d03f` FOREIGN KEY (`resource_ptr_id`) REFERENCES `home_resource` (`id`);

--
-- Constraints for table `home_pad`
--
ALTER TABLE `home_pad`
  ADD CONSTRAINT `requested_antenna_id_refs_resource_ptr_id_f8b00e53` FOREIGN KEY (`requested_antenna_id`) REFERENCES `home_antenna` (`resource_ptr_id`),
  ADD CONSTRAINT `current_antenna_id_refs_resource_ptr_id_f8b00e53` FOREIGN KEY (`current_antenna_id`) REFERENCES `home_antenna` (`resource_ptr_id`),
  ADD CONSTRAINT `resource_ptr_id_refs_id_f236381` FOREIGN KEY (`resource_ptr_id`) REFERENCES `home_resource` (`id`);

--
-- Constraints for table `home_resource`
--
ALTER TABLE `home_resource`
  ADD CONSTRAINT `requester_id_refs_id_3f03bd43` FOREIGN KEY (`requester_id`) REFERENCES `auth_user` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
