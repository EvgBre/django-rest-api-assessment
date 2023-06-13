from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist
from django.db.models import Count


        
class ArtistView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
       """GET Single Artist"""
        # Retrieve the artist object with the specified primary key (pk)
       artist = Artist.objects.annotate(
            # Annotate the queryset with the song_count, which is the count of songs for each artist
            song_count=Count('songs')
        ).get(pk=pk)

        # Create a serialized representation of the artist object using the ArtistSerializer
       serializer = ArtistSerializer(artist)

        # Return the serialized artist object as a JSON response with a 200 OK status code
       return Response(serializer.data, status=status.HTTP_200_OK) 

    def list(self, request):
        """GET All Artists"""
        artists = Artist.objects.annotate(song_count=Count('songs')).all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """

        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"],
        )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]
        artist.save()
        
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    song_count = serializers.IntegerField(default=None)
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')
        depth=1