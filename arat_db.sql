-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 07, 2013 at 06:32 PM
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=46 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=18 ;

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=16 ;

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

-- --------------------------------------------------------

--
-- Table structure for table `home_antenna`
--

DROP TABLE IF EXISTS `home_antenna`;
CREATE TABLE IF NOT EXISTS `home_antenna` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(5) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `current_ste` int(11) DEFAULT NULL,
  `requested_ste` int(11) DEFAULT NULL,
  `requester_id` int(11) DEFAULT NULL,
  `request_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `home_antenna_b8ca8b9f` (`requester_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=66 ;

-- --------------------------------------------------------

--
-- Table structure for table `home_centrallo`
--

DROP TABLE IF EXISTS `home_centrallo`;
CREATE TABLE IF NOT EXISTS `home_centrallo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `line` int(11) NOT NULL,
  `assigned` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `current_antenna_id` int(11) DEFAULT NULL,
  `requested_antenna_id` int(11) DEFAULT NULL,
  `requester_id` int(11) DEFAULT NULL,
  `request_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `line` (`line`),
  UNIQUE KEY `current_antenna_id` (`current_antenna_id`),
  KEY `home_centrallo_62753b47` (`requested_antenna_id`),
  KEY `home_centrallo_b8ca8b9f` (`requester_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=74 ;

-- --------------------------------------------------------

--
-- Table structure for table `home_correlatorconfiguration`
--

DROP TABLE IF EXISTS `home_correlatorconfiguration`;
CREATE TABLE IF NOT EXISTS `home_correlatorconfiguration` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `line` int(11) NOT NULL,
  `correlator` longtext NOT NULL,
  `assigned` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `current_antenna_id` int(11) DEFAULT NULL,
  `requested_antenna_id` int(11) DEFAULT NULL,
  `requester_id` int(11) DEFAULT NULL,
  `request_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `line` (`line`),
  KEY `home_correlatorconfiguration_38f06868` (`current_antenna_id`),
  KEY `home_correlatorconfiguration_62753b47` (`requested_antenna_id`),
  KEY `home_correlatorconfiguration_b8ca8b9f` (`requester_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=85 ;

-- --------------------------------------------------------

--
-- Table structure for table `home_pad`
--

DROP TABLE IF EXISTS `home_pad`;
CREATE TABLE IF NOT EXISTS `home_pad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `line` int(11) NOT NULL,
  `location` longtext NOT NULL,
  `assigned` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `current_antenna_id` int(11) DEFAULT NULL,
  `requested_antenna_id` int(11) DEFAULT NULL,
  `requester_id` int(11) DEFAULT NULL,
  `request_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `line` (`line`),
  UNIQUE KEY `current_antenna_id` (`current_antenna_id`),
  KEY `home_pad_62753b47` (`requested_antenna_id`),
  KEY `home_pad_b8ca8b9f` (`requester_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=203 ;

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
-- Constraints for table `home_centrallo`
--
ALTER TABLE `home_centrallo`
  ADD CONSTRAINT `requester_id_refs_id_d5f6f202` FOREIGN KEY (`requester_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `current_antenna_id_refs_id_e50c0ce` FOREIGN KEY (`current_antenna_id`) REFERENCES `home_antenna` (`id`),
  ADD CONSTRAINT `requested_antenna_id_refs_id_e50c0ce` FOREIGN KEY (`requested_antenna_id`) REFERENCES `home_antenna` (`id`);

--
-- Constraints for table `home_correlatorconfiguration`
--
ALTER TABLE `home_correlatorconfiguration`
  ADD CONSTRAINT `requester_id_refs_id_f0c6c71d` FOREIGN KEY (`requester_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `current_antenna_id_refs_id_ae9034c7` FOREIGN KEY (`current_antenna_id`) REFERENCES `home_antenna` (`id`),
  ADD CONSTRAINT `requested_antenna_id_refs_id_ae9034c7` FOREIGN KEY (`requested_antenna_id`) REFERENCES `home_antenna` (`id`);

--
-- Constraints for table `home_pad`
--
ALTER TABLE `home_pad`
  ADD CONSTRAINT `requester_id_refs_id_24362f31` FOREIGN KEY (`requester_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `current_antenna_id_refs_id_f8b00e53` FOREIGN KEY (`current_antenna_id`) REFERENCES `home_antenna` (`id`),
  ADD CONSTRAINT `requested_antenna_id_refs_id_f8b00e53` FOREIGN KEY (`requested_antenna_id`) REFERENCES `home_antenna` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
