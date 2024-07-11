-- Drop the procedure if it already exists to prevent errors during redefinition
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Define the delimiter to allow semicolons within the procedure body
DELIMITER $$

-- Create the ComputeAverageWeightedScoreForUsers procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Temporarily rename 'users' table to 'U' for clarity within the query
    SET @old_users_name = 'users';
    RENAME TABLE users TO U;

    -- Perform the weighted average calculation and update operation
    UPDATE U
    INNER JOIN (
        SELECT U.id, SUM(C.score * P.weight) / SUM(P.weight) AS weighted_average
        FROM U
        JOIN corrections AS C ON U.id = C.user_id
        JOIN projects AS P ON C.project_id = P.id
        GROUP BY U.id
    ) AS WeightedAverages ON U.id = WeightedAverages.id
    SET U.average_score = WeightedAverages.weighted_average;

    -- Restore the original 'users' table name
    RENAME TABLE U TO users;
END$$

-- Reset the delimiter to its default state
DELIMITER ;
