-- Create a trigger to update the valid email attribute upon each update on user's email.
DROP TRIGGER IF EXISTS valid_email;
DELIMITER //
CREATE TRIGGER valid_email BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email = OLD.email THEN
        SET NEW.valid_email = NEW.valid_email;
    ELSE
        SET NEW.valid_email = 0;
    END IF;
END//
DELIMITER ;
