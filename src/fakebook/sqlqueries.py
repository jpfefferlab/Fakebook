# This file stores the sqlite queries required to create the downloadable .xlsx file

def get_query(table):
    
    if table == "user":
        return "SELECT profiles_profile.id AS \"user_id\", auth_user.username, profiles_profile.first_name, profiles_profile.last_name, profiles_profile.avatar, profiles_profile.bio, auth_user.date_joined, auth_user.last_login "\
                "FROM profiles_profile, auth_user "\
                "WHERE profiles_profile.user_id = auth_user.id"

    if table == "friends":
        return "SELECT sender_id, receiver_id, status, updated, created "\
                "FROM profiles_relationship"

    if table == "chats":
        return "SELECT source_user.username AS \"source_user\", target_user.username AS \"target_user\", chat_message.content, chat_message.date " \
               "FROM chat_message, chat_chat, profiles_profile source_profile, auth_user source_user, profiles_profile target_profile, auth_user target_user " \
               "WHERE chat_message.chat_id = chat_chat.id AND chat_message.user_id = source_profile.id AND source_profile.user_id = source_user.id " \
               "AND target_profile.id <> chat_message.user_id AND ( target_profile.id = chat_chat.user_1_id OR target_profile.id = chat_chat.user_2_id ) AND target_profile.user_id = target_user.id"

    if table == "sessions":
        return "SELECT auth_user.username, profile_id, first_seen, last_seen "\
               "FROM analytics_trackedsession, profiles_profile, auth_user "\
               "WHERE analytics_trackedsession.profile_id = profiles_profile.id AND profiles_profile.user_id = auth_user.id"

    if table == "post-views":
        return "SELECT auth_user.username, profile_id, post_id, total_time_ms " \
               "FROM analytics_trackedpostview, profiles_profile, auth_user " \
               "WHERE analytics_trackedpostview.profile_id = profiles_profile.id AND profiles_profile.user_id = auth_user.id"

    if table == "posts":
        return "SELECT posts_post.id AS \"post_id\", posts_post.author_id, posts_post.content, posts_post.created, posts_post.image, "\
		        "(SELECT COUNT(*) "\
		        "FROM posts_comment "\
		        "WHERE posts_post.id = posts_comment.post_id) AS \"comments\", "\
		        "(SELECT COUNT(*) "\
		        "FROM posts_post_liked "\
		        "WHERE posts_post.id = posts_post_liked.post_id) AS \"likes_received\", "\
		        "(SELECT COUNT(*) "\
		        "FROM posts_post_disliked "\
		        "WHERE posts_post.id = posts_post_disliked.post_id) AS \"dislikes_received\", "\
		        "(SELECT COUNT(*) "\
		        "FROM posts_post_reported "\
		        "WHERE posts_post.id = posts_post_reported.post_id) AS \"reports_received\" "\
                "FROM posts_post"

    if table == "comments":
        return "SELECT id AS \"comment_id\", post_id, user_id, body AS \"content\", created, updated "\
                "FROM posts_comment"
    
    if table == "likes":
        return "SELECT post_id, user_id, value, updated, created "\
                "FROM posts_like"
    
    if table  == "dislikes":
        return "SELECT post_id, user_id, value, updated, created "\
                "FROM posts_dislike"
    
    if table == "reports":
        return "SELECT post_id, user_id, value, updated, created "\
                "FROM posts_report"

    if table == "advertisements":
        return "SELECT advertisement_id, text, url, num_clicked, image, profile_id "\
                "FROM advertisements_advertisement, advertisements_advertisement_user_clicked "\
                "WHERE advertisements_advertisement.id = advertisement_id"