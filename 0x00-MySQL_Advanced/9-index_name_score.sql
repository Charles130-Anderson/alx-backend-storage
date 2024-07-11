-- Add an index on the first letter of name and score column
-- This index improves performance for queries involving filtering or sorting by name and score.

CREATE INDEX idx_name_first_score ON names (name(1), score);
