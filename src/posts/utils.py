
from django.utils.translation import pgettext

def format_likes_string(usernames, entries_to_show):
    total_count = len(usernames)
    if total_count > entries_to_show:
        usernames = usernames[:(entries_to_show - 1)]
    string = "\n".join(usernames)
    if total_count > entries_to_show:
        # string += f"\nand {total_count - (entries_to_show - 1)} more"
        string += pgettext({"additional_count": total_count - (entries_to_show - 1)}, "additional-likes-format")
    return string

