-- Creates a stored procedure ComputeAverageScoreForUser
-- that computes and stores the average score for a student
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN p_user_id INT)
BEGIN
    -- Calculate the average score for the given user
    UPDATE users
    SET average_score = (
        SELECT AVG(score) AS avg_score
        FROM corrections
        WHERE user_id = p_user_id
    );
END$$

DELIMITER ;
