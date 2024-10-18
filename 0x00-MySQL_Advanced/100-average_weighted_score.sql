-- Write a SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser
(IN user_id INT)
BEGIN
  UPDATE users
  SET average_score = (
    SELECT (SUM(cs.score * ps.weight) / SUM(ps.weight))
    FROM corrections AS cs INNER JOIN projects AS ps 
    ON cs.project_id=ps.id
    WHERE cs.user_id=users.id
  )
  WHERE id=user_id;
END$$

DELIMITER ;
