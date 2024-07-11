-- Define the ComputeAverageWeightedScoreForUser stored procedure
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE avg_weighted_score FLOAT;
    
    -- Calculate the average weighted score
    SELECT SUM(C.score * P.weight) / SUM(P.weight) INTO avg_weighted_score
    FROM corrections AS C
    INNER JOIN projects AS P ON C.project_id = P.id
    WHERE C.user_id = p_user_id;
    
    -- Update the users table with the computed average weighted score
    UPDATE users
    SET average_score = avg_weighted_score
    WHERE id = p_user_id;
END$$
DELIMITER ;
