CREATE TABLE regional_stats (
    id SERIAL PRIMARY KEY,
    region TEXT,
    metric TEXT,
    value FLOAT,
    year INT,
    source_page INT
);