-- STORED PROCEDURE: ComputeAverageWeightedScoreForUsers THAT CALCULATES THE AVERAGE WEIGHTED SCORE FOR ALL USERS.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER //
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
  UPDATE users AS user,
    (SELECT user.id, SUM(score * weight) / SUM(weight) AS score
    FROM users AS user
    JOIN corrections as correction ON user.id=correction.user_id
    JOIN projects AS project ON correction.project_id=project.id
    GROUP BY user.id)
  AS average_weighted_scores
  SET user.average_score = average_weighted_scores.score
  WHERE user.id=average_weighted_scores.id;
END//
DELIMITER ;
