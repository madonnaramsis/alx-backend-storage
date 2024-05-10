-- Create index on first letter of the name and score columns in this sequence.
CREATE INDEX idx_name_first_score ON names(name(1), score);
