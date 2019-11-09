CREATE TABLE IF NOT EXISTS `pii` (
  id              INT          AUTO_INCREMENT PRIMARY KEY,
  js_documents_id VARCHAR(256) NOT NULL,
  individual_id   CHAR(36)     NOT NULL,
  pii_json        JSON         NULL
) COMMENT 'used to store masked data from resumes for future data analysis';
