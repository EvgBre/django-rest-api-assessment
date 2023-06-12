from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Song, Artist, SongGenre

class SongView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single event"""
        
        try:
            song = Song.objects.get('genres').get(pk=pk) 
            serializer = SongSerializer(song, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Artist.DoesNotExist:
            return Response({'message': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
      songs = Song.objects.all()
      
      # filter to query songs by artist_id
      artist = request.query_params.get('artist_id', None)
      if artist is not None:
          songs = songs.filter(artist_id_id=artist)
          
      serializer = SongSerializer(songs, many=True)
      return Response(serializer.data)
    
    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        artist_id = Artist.objects.get(pk=request.data["artistId"])
        
        song = Song.objects.create(
            title=request.data["title"],
            artist_id=artist_id,
            album=request.data["album"],
            length=request.data["length"]
        )

        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        """Handle PUT requests for a game

        Returns:
            Response -- Empty body with 204 status code
        """

        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.album = request.data["album"]
        song.length = request.data["length"]

        artist_id = Artist.objects.get(pk=request.data["artistId"])
        song.artist_id = artist_id
        song.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk):
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
    
class SongGenreSerializer(serializers.ModelSerializer):
  class Meta:
      model = SongGenre
      fields = ( 'genre_id', )
      depth = 1
class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for game types
    """
    genres = SongGenreSerializer(many=True, read_only=True)
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length', 'genres')
        depth=1