-- Drop the procedure if it exists
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

-- Delimiter to change the delimiter from ;
DELIMITER //

-- Create the procedure
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id_var INT;
    DECLARE user_name VARCHAR(255);
    DECLARE project_weight INT;
    DECLARE total_score FLOAT;
    DECLARE weighted_score FLOAT;
    DECLARE total_weight INT;
    
    -- Declare cursor for iterating through users
    DECLARE cur CURSOR FOR 
        SELECT id, name FROM users;
        
    -- Declare continue handler to exit loop
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    -- Open the cursor
    OPEN cur;
    
    -- Start processing rows
    read_loop: LOOP
        -- Fetch next user_id and user_name from cursor into variables
        FETCH cur INTO user_id_var, user_name;
        
        -- Exit loop if no more rows
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        -- Initialize variables for calculating weighted average
        SET total_score = 0;
        SET weighted_score = 0;
        SET total_weight = 0;
        
        -- Calculate total weighted score and total weight for the user
        SELECT SUM(c.score * p.weight), SUM(p.weight)
        INTO total_score, total_weight
        FROM corrections c
        JOIN projects p ON c.project_id = p.id
        WHERE c.user_id = user_id_var;
        
        -- Calculate weighted average score if total_weight > 0
        IF total_weight > 0 THEN
            SET weighted_score = total_score / total_weight;
        ELSE
            SET weighted_score = 0;
        END IF;
        
        -- Update the user's average_score in the users table
        UPDATE users SET average_score = weighted_score WHERE id = user_id_var;
        
    END LOOP; -- End of read_loop
    
    -- Close the cursor
    CLOSE cur;
    
END //

-- Reset the delimiter
DELIMITER ;

-- Call the procedure to compute and update the average weighted scores
CALL ComputeAverageWeightedScoreForUsers();
