-- Write a SQL script that creates a stored procedure
-- ComputeAverageWeightedScoreForUsers that computes and store the average
-- weighted score for all students.

DELIMITER $$
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers$$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers
()
BEGIN
  UPDATE users
  SET average_score = (
    SELECT (SUM(cs.score * ps.weight) / SUM(ps.weight))
    FROM corrections AS cs INNER JOIN projects AS ps
    ON cs.project_id=ps.id
    WHERE cs.user_id=users.id
  )
  ORDER BY id;
END$$

DELIMITER ;
