-- todo: figure out how to create table in db given another connection
-- CREATE DATABASE veryfidev;

CREATE TABLE IF NOT EXISTS documents (
    document_id SERIAL PRIMARY KEY,
    ml_response VARCHAR (2048)
);

CREATE TABLE IF NOT EXISTS parsed_total (
    id SERIAL PRIMARY KEY,
    document_id INT,
    business_id SMALLINT,
    value SMALLINT,
    score NUMERIC(2),
    ocr_score NUMERIC(2),
    bounding_box NUMERIC(2) ARRAY[4],
    CONSTRAINT fk_document
      FOREIGN KEY(document_id)
	  REFERENCES documents(document_id)
	  ON DELETE CASCADE
);

CREATE INDEX title_idx ON parsed_total (business_id);
