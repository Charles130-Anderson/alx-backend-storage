-- Creates a stored procedure ComputeAverageScoreForUser
-- that computes and stores the average score for a student
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE num_corrections INT;

    SELECT SUM(score), COUNT(*) INTO total_score, num_corrections
    FROM corrections
    WHERE user_id = ComputeAverageScoreForUser.user_id;

    IF num_corrections > 0 THEN
        UPDATE users
        SET average_score = total_score / num_corrections
        WHERE id = ComputeAverageScoreForUser.user_id;
    ELSE
        UPDATE users
        SET average_score = 0
        WHERE id = ComputeAverageScoreForUser.user_id;
    END IF;
END $$
DELIMITER ;
