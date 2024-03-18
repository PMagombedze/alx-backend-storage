-- user_id, a users.id value (you can assume user_id is linked to an existing users)
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(user_id INT)
BEGIN
    DECLARE w_avg_score FLOAT;

    SELECT SUM(score * weight) / SUM(weight) INTO w_avg_score
    FROM users AS U
    JOIN corrections AS C ON U.id = C.user_id
    JOIN projects AS P ON C.project_id = P.id
    WHERE U.id = user_id;

    UPDATE users SET average_score = w_avg_score WHERE id = user_id;
END
$$

DELIMITER ;
