chat_room_list_query = """SELECT uuid, nickname, id, image
FROM
(
    SELECT room_uuid as uuid, nickname, pp_id as id, image
    FROM
    (
        SELECT U0.room_uuid as room_uuid, P0.nickname as nickname, PP0.id as pp_id, PP0.image AS image, ROW_NUMBER() OVER (PARTITION BY PP0.user_id ORDER BY PP0.main DESC, PP0.id ASC) pp_order
        FROM
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
            ) U0
            INNER JOIN
            user_profile_profile P0 ON P0.user_id = U0.user_id
            LEFT JOIN
            profile_picture_profilepicture PP0 ON PP0.user_id = U0.user_id
    ) WHERE pp_order = 1
)"""
