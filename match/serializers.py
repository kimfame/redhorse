import logging

from datetime import date

from django.conf import settings
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from match.models import Match
from user_profile.models import Profile


logger = logging.getLogger(__name__)


class MatchSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    is_liked = serializers.BooleanField()

    def create(self, validated_data):
        def cross_check_match(new_match: Match) -> None:
            try:
                with transaction.atomic():
                    cross_match = Match.objects.filter(
                        sender=new_match.receiver,
                        receiver=new_match.sender,
                        is_liked=True,
                        is_matched=False,
                    ).first()

                    if cross_match:
                        cross_match.is_matched = True
                        new_match.is_matched = True

                        cross_match.save()
                        # create_chat_room(sender, receiver)
                    new_match.save()

            except IntegrityError as e:
                logger.error(e)
                raise serializers.ValidationError(
                    {"error": ["시스템 에러로 인해 Like를 보낼 수 없습니다. 추후 다시 시도해주세요."]}
                )

        sender = self.context.get("user")

        if (
            Match.objects.filter(
                sender=sender,
                created_at__date=date.today(),
            ).count()
            >= settings.MAX_LIKE_NUM
        ):
            raise serializers.ValidationError({"error": ["오늘은 더이상 Like를 보낼 수 없습니다."]})

        receiver_profile = get_object_or_404(
            Profile.objects.select_related("user"),
            uuid=validated_data.get("uuid"),
        )
        receiver = receiver_profile.user

        if Match.objects.filter(sender=sender, receiver=receiver).exists():
            raise serializers.ValidationError({"receiver": ["Like를 이미 보낸 유저입니다."]})

        is_liked = validated_data.get("is_liked")

        new_match = Match(
            sender=sender,
            receiver=receiver,
            is_liked=is_liked,
        )

        if is_liked:
            cross_check_match(new_match)
        else:
            new_match.save()

        return new_match

    def validate_uuid(self, value):
        user = self.context.get("user")

        if user.profile.uuid == value:
            raise serializers.ValidationError("잘못된 Like 요청입니다.")
        else:
            return value
