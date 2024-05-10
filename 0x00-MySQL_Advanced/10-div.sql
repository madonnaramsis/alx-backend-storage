-- Create a function that divides 2 numbers then return the result or 0 if the second number is 0.
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER //
CREATE FUNCTION SafeDiv(
  a FLOAT,
  b FLOAT
)
RETURNS FLOAT
BEGIN
  IF b = 0 THEN
    RETURN 0;
  ELSE
    RETURN a / b;
  END IF;
END//
DELIMITER ;
