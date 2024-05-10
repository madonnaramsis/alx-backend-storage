-- Creates need_meeting view.
DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS SELECT name FROM students WHERE score < 80 AND (last_meeting IS NULL OR last_meeting < SUBDATE(CURDATE(), INTERVAL 1 MONTH));
