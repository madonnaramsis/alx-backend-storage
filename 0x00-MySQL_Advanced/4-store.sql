-- Create a trigger to decrease the quantiy of the item after adding a new order.
DROP TRIGGER IF EXISTS qty_after_order;
DELIMITER //
CREATE TRIGGER qty_after_order AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
        SET quantity = quantity - NEW.number
        WHERE name = NEW.item_name;
END//
DELIMITER ;
