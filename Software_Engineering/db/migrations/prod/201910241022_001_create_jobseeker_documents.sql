CREATE TABLE IF NOT EXISTS `jobseeker_documents` (
  `id`                VARCHAR(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `individual_id`     CHAR(36) COLLATE utf8mb4_unicode_ci NOT NULL,
  `file_name`         VARCHAR(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `file_extension`    VARCHAR(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `file_size`         INT(11) DEFAULT NULL,
  `document_category` VARCHAR(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_default`        TINYINT(1) DEFAULT NULL,
  `file_path`         VARCHAR(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_by`        VARCHAR(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_on`        datetime DEFAULT NULL,
  `modified_by`       VARCHAR(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `modified_on`       datetime DEFAULT NULL,
  `is_deleted`        TINYINT(1) DEFAULT '0',
  `parsed_content`    LONGTEXT COLLATE utf8mb4_unicode_ci,
  `parsed_content_v2` LONGTEXT COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`) 
) COMMENT 'replica of table from mcf as of oct 2019';