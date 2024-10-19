import re
from rest_framework import serializers

YOUTUBE_REGEX = r'^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$'

def validate_video_url(value):
    if not re.match(YOUTUBE_REGEX, value):
        raise serializers.ValidationError("Разрешены только ссылки на youtube.com.")
    return value