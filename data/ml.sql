/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50537
Source Host           : localhost:3306
Source Database       : ml

Target Server Type    : MYSQL
Target Server Version : 50537
File Encoding         : 65001

Date: 2017-10-17 22:33:42
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `raw_test`
-- ----------------------------
DROP TABLE IF EXISTS `raw_test`;
CREATE TABLE `raw_test` (
  `age` varchar(100) DEFAULT NULL,
  `workclass` varchar(100) DEFAULT NULL,
  `fnlwgt` varchar(100) DEFAULT NULL,
  `education` varchar(100) DEFAULT NULL,
  `education_num` varchar(100) DEFAULT NULL,
  `marital_status` varchar(100) DEFAULT NULL,
  `occupation` varchar(100) DEFAULT NULL,
  `relationship` varchar(100) DEFAULT NULL,
  `race` varchar(100) DEFAULT NULL,
  `sex` varchar(100) DEFAULT NULL,
  `capital_gain` varchar(100) DEFAULT NULL,
  `capital_loss` varchar(100) DEFAULT NULL,
  `hours_per_week` varchar(100) DEFAULT NULL,
  `native_country` varchar(100) DEFAULT NULL,
  `comment` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of raw_test
-- ----------------------------

-- ----------------------------
-- Table structure for `raw_train`
-- ----------------------------
DROP TABLE IF EXISTS `raw_train`;
CREATE TABLE `raw_train` (
  `age` varchar(100) DEFAULT NULL,
  `workclass` varchar(100) DEFAULT NULL,
  `fnlwgt` varchar(100) DEFAULT NULL,
  `education` varchar(100) DEFAULT NULL,
  `education_num` varchar(100) DEFAULT NULL,
  `marital_status` varchar(100) DEFAULT NULL,
  `occupation` varchar(100) DEFAULT NULL,
  `relationship` varchar(100) DEFAULT NULL,
  `race` varchar(100) DEFAULT NULL,
  `sex` varchar(100) DEFAULT NULL,
  `capital_gain` varchar(100) DEFAULT NULL,
  `capital_loss` varchar(100) DEFAULT NULL,
  `hours_per_week` varchar(100) DEFAULT NULL,
  `native_country` varchar(100) DEFAULT NULL,
  `comment` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of raw_train
-- ----------------------------
