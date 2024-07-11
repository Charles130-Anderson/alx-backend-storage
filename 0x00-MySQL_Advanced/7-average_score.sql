-- Drop the procedure if it already exists to avoid errors during creation
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Set the delimiter to $$ to allow semicolons within the procedure body
DELIMITER $$

-- Create the ComputeAverageScoreForUser procedure
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    -- Update the average_score of the user with the calculated average score from their corrections
    UPDATE users
    SET average_score = (
        -- Select the average score from the corrections table where the user_id matches
        SELECT AVG(score) FROM corrections AS C WHERE C.user_id = user_id
    )
    -- Ensure the update applies to the correct user by matching the user_id
    WHERE id = user_id;
END$$

-- Reset the delimiter to ; after defining the procedure
DELIMITER ;
