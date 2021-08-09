/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 80023
 Source Host           : localhost:3306
 Source Schema         : demo

 Target Server Type    : MySQL
 Target Server Version : 80023
 File Encoding         : 65001

 Date: 09/08/2021 16:13:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for cases
-- ----------------------------
DROP TABLE IF EXISTS `cases`;
CREATE TABLE `cases`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `i_id` int(0) UNSIGNED NULL DEFAULT NULL,
  `priority` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '优先级',
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '标题',
  `enter` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `outs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `result` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '实际结果',
  `created` datetime(0) NULL DEFAULT NULL,
  `created_by` int(0) UNSIGNED NULL DEFAULT NULL,
  `updated` datetime(0) NULL DEFAULT NULL,
  `updated_by` int(0) UNSIGNED NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `case_ib`(`i_id`) USING BTREE,
  INDEX `created_by`(`created_by`) USING BTREE,
  INDEX `updated_by`(`updated_by`) USING BTREE,
  CONSTRAINT `case_ib` FOREIGN KEY (`i_id`) REFERENCES `interface` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `cases_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `cases_ibfk_2` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of cases
-- ----------------------------
INSERT INTO `cases` VALUES (25, 99, 'P0', '添加文章冒烟测试用例', '{\'content\': \'今天天气真好！\'}', '{\'response\': {\'code\': 200, \'msg\': \'success\'}}', '{\"success\":true,\"code\":\"200\",\"msg\":\"success\",\"data\":null}', '2021-08-06 11:10:21', 45, NULL, NULL, 'auto');
INSERT INTO `cases` VALUES (26, 99, 'P1', '添加文章content最大长度校验', '{\'content\': \'今天天气真好！今天天气真好！今天天气真\'}', '{\'response\': {\'code\': 200, \'msg\': \'success\'}}', '{\"success\":true,\"code\":\"200\",\"msg\":\"success\",\"data\":null}', '2021-08-06 11:10:21', 45, NULL, NULL, 'auto');
INSERT INTO `cases` VALUES (27, 99, 'P2', '添加文章content最大长度校验', '{\'content\': \'今天天气真好！今天天气真好！今天天气真好\'}', '{\'response\': {\'code\': \'P00001\', \'msg\': \'fail\'}}', NULL, '2021-08-06 11:10:21', 45, NULL, NULL, 'auto');
INSERT INTO `cases` VALUES (28, 99, 'P1', '添加文章content必填校验', '{\'content\': \'\'}', '{\'response\': {\'code\': 200, \'msg\': \'success\'}}', NULL, '2021-08-06 11:10:21', 45, NULL, NULL, 'auto');

-- ----------------------------
-- Table structure for interface
-- ----------------------------
DROP TABLE IF EXISTS `interface`;
CREATE TABLE `interface`  (
  `id` int(0) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '接口名称',
  `methods` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '请求方式',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '请求路径',
  `login_required` tinyint(0) NULL DEFAULT NULL COMMENT '是否需要登录',
  `params` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created` timestamp(0) NULL DEFAULT NULL,
  `created_by` int(0) UNSIGNED NULL DEFAULT NULL,
  `updated` timestamp(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0),
  `updated_by` int(0) UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `name`(`name`) USING BTREE,
  INDEX `create_user`(`created_by`) USING BTREE,
  INDEX `operate_user`(`updated_by`) USING BTREE,
  CONSTRAINT `create_user` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `operate_user` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 100 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of interface
-- ----------------------------
INSERT INTO `interface` VALUES (99, '添加文章', 'post', '/articles/save', 1, NULL, '2021-08-03 15:39:12', 1, '2021-08-06 11:08:20', 1);

-- ----------------------------
-- Table structure for params
-- ----------------------------
DROP TABLE IF EXISTS `params`;
CREATE TABLE `params`  (
  `id` int(0) UNSIGNED NOT NULL AUTO_INCREMENT,
  `i_id` int(0) UNSIGNED NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `case1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `maxlength` int(0) NULL DEFAULT NULL,
  `minlength` int(0) NULL DEFAULT NULL,
  `required` tinyint(1) NULL DEFAULT NULL,
  `options` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created` timestamp(0) NULL DEFAULT NULL,
  `created_by` int(0) UNSIGNED NULL DEFAULT NULL,
  `updated` timestamp(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0),
  `updated_by` int(0) UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `interface_id`(`i_id`) USING BTREE,
  INDEX `created_by`(`created_by`) USING BTREE,
  INDEX `updated_by`(`updated_by`) USING BTREE,
  CONSTRAINT `params_ibfk_1` FOREIGN KEY (`i_id`) REFERENCES `interface` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `params_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `params_ibfk_3` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of params
-- ----------------------------
INSERT INTO `params` VALUES (18, 99, 'content', '今天天气真好！', 20, NULL, 0, NULL, '2021-08-03 15:39:56', 1, '2021-08-03 16:05:14', 1);

-- ----------------------------
-- Table structure for systems
-- ----------------------------
DROP TABLE IF EXISTS `systems`;
CREATE TABLE `systems`  (
  `id` int(0) UNSIGNED NOT NULL AUTO_INCREMENT,
  `s_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `val` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `created` datetime(0) NULL DEFAULT NULL,
  `created_by` int(0) UNSIGNED NULL DEFAULT NULL,
  `updated` datetime(0) NULL DEFAULT NULL,
  `updated_by` int(0) UNSIGNED NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '数据类型',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `created_by`(`created_by`) USING BTREE,
  INDEX `updated_by`(`updated_by`) USING BTREE,
  CONSTRAINT `systems_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `systems_ibfk_2` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of systems
-- ----------------------------
INSERT INTO `systems` VALUES (1, 'url', 'http://192.168.3.66:9003', '2021-08-04 17:29:50', NULL, NULL, NULL, 'sys_var');
INSERT INTO `systems` VALUES (2, 'name', 'jack', '2021-08-04 18:01:28', 45, NULL, NULL, 'user_var');
INSERT INTO `systems` VALUES (3, 'Cookie', 'SESSION=Nzc2NzNkZDgtODBkMi00N2M4LTg1YTctOWYxZGI5NmM3ZGFi', '2021-08-06 10:07:15', NULL, NULL, NULL, 'request_headers');
INSERT INTO `systems` VALUES (4, 'token', '77673dd8-80d2-47c8-85a7-9f1db96c7dab', '2021-08-06 10:07:43', NULL, NULL, NULL, 'request_headers');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int(0) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `created` timestamp(0) NULL DEFAULT NULL,
  `updated` timestamp(0) NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP(0),
  `created_by` int(0) UNSIGNED NULL DEFAULT NULL,
  `updated_by` int(0) UNSIGNED NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 69 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', '123456', NULL, NULL, NULL, NULL);
INSERT INTO `users` VALUES (45, 'test', '123456', NULL, NULL, NULL, NULL);

SET FOREIGN_KEY_CHECKS = 1;
