from rest_framework import viewsets, status
from rest_framework.response import Response

from match.serializers import MatchSerializer


class MatchViewSet(viewsets.ViewSet):
    def create(self, request):
        user = request.user
        serializer = MatchSerializer(context={"user": user}, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
