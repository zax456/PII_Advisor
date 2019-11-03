CREATE TABLE IF NOT EXISTS tmp
(
  tmp_id      INT            auto_increment PRIMARY KEY,
  created_at  DATETIME       NULL,
  file_path   VARCHAR(500)   NULL,
  data        VARCHAR(5000)  NOT NULL
) COMMENT 'used for transaction audits';
