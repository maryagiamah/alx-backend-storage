-- Write a SQL script that creates a trigger that resets
-- the attribute valid_email only when the email hasi been changed.

DELIMITER $$

DROP TRIGGER IF EXISTS update_email$$

CREATE TRIGGER update_email
BEFORE UPDATE 
ON users FOR EACH ROW
BEGIN
  IF OLD.email != NEW.email
  THEN
    SET NEW.valid_email = 0;
  END IF;
END $$

DELIMITER ;
