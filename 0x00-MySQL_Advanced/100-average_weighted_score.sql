-- STORED PROCEDURE: ComputeAverageWeightedScoreForUser THAT TAKES A user_id AS INPUT AND CALCULATES THE AVERAGE WEIGHTED SCORE FOR THAT USER. THE AVERAGE WEIGHTED SCORE IS CALCULATED BY MULTIPLYING THE SCORE OF EACH CORRECTION BY THE WEIGHT OF THE PROJECT AND THEN DIVIDING THE SUM OF THESE VALUES BY THE SUM OF THE WEIGHTS OF THE PROJECTS.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
  user_id INT
)
BEGIN
  DECLARE total_score FLOAT;
  DECLARE total_weight FLOAT;
  SET total_score = (SELECT SUM(score * weight) FROM corrections
                      JOIN projects ON corrections.project_id = projects.id
                      WHERE corrections.user_id = user_id);
  SET total_weight = (SELECT SUM(weight) FROM corrections
                      JOIN projects ON corrections.project_id = projects.id
                      WHERE corrections.user_id = user_id);
  IF total_weight IS NULL THEN
    SET total_weight = 0;
  END IF;
  IF total_score IS NULL THEN
    SET total_score = 0;
  END IF;
  IF total_weight = 0 THEN
    SET total_weight = 1;
  END IF;
  UPDATE users
  SET users.average_score = total_score / total_weight
  WHERE users.id = user_id;
END//
DELIMITER ;
