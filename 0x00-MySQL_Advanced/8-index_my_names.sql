-- Import the names.sql file into the database first
-- Assuming you've already imported it

-- Create index idx_name_first on the first letter of name in the names table
CREATE INDEX idx_name_first ON names (LEFT(name, 1));
