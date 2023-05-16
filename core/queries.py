chat_room_list_query = """SELECT uuid, nickname, id, image
FROM
(
    SELECT room_uuid as uuid, nickname, pp_id as id, image
    FROM
    (
        SELECT room_uuid, P0.nickname as nickname, PP0.id as pp_id, PP0.image AS image, ROW_NUMBER() OVER (PARTITION BY PP0.profile_id ORDER BY PP0.main DESC, PP0.id ASC) profile_picture_order
        FROM
            user_profile_profile P0
            INNER JOIN
            (
                SELECT room_uuid, user_id, user_order FROM 
                (
                    SELECT R0.uuid as room_uuid, M1.user_id as user_id, ROW_NUMBER() OVER (PARTITION BY R0.id ORDER BY M1.user_id DESC) user_order
                    FROM chat_room_chatroom R0, chat_room_chatroommember M1
                    WHERE
                        M1.user_id <> %(id)s
                        AND R0.id IN 
                        (
                            SELECT M0.room_id FROM chat_room_chatroommember M0 WHERE M0.is_active AND M0.user_id = %(id)s
                        )
                        AND R0.id = M1.room_id
                ) WHERE user_order = 1
            ) CU ON CU.user_id = P0.user_id
            LEFT JOIN
            profile_picture_profilepicture PP0 ON P0.id = PP0.profile_id
    ) WHERE profile_picture_order = 1
)"""

feed_exclusion_list = """SELECT sender_id AS user_id
FROM match_match
WHERE receiver_id = %(id)s
UNION
SELECT receiver_id AS user_id
FROM match_match
WHERE sender_id = %(id)s;
"""
