from rest_framework import serializers
from django.utils.timesince import timesince
from tweets.models import Tweet
from accounts.api.serializers import UserDisplaySerializer

class ParentTweetModelSerializer(serializers.ModelSerializer):
	user = UserDisplaySerializer(read_only=True)
	date_display = serializers.SerializerMethodField()
	timesince = serializers.SerializerMethodField()
	likes = serializers.SerializerMethodField()
	did_like = serializers.SerializerMethodField()

	class Meta:
		model = Tweet
		fields = [
			'id',
			'user',
			'content',
			'timestamp',
			'date_display',
			'timesince',
            'likes',
            'did_like',
		]

	def get_did_like(self, obj):
		try:
			user = request.user
			if user.is_authenticated():
				if user in obj.liked.all():
					return True
		except:
			pass
		return False

	def get_likes(self, obj):
		return obj.liked.all().count()

	def get_date_display(self, obj):
		return obj.timestamp.strftime("%b %d, %Y | at %I:%M %p")

	def get_timesince(self, obj):
		return timesince(obj.timestamp) + " ago"

class TweetModelSerializer(serializers.ModelSerializer):
    parent_id = serializers.CharField(write_only=True, required=False)
    user = UserDisplaySerializer(read_only=True)
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()
    parent = ParentTweetModelSerializer()
    likes = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()

    class Meta:
    	model = Tweet
    	fields = [
    		'parent_id',
    		'id',
    		'user',
    		'content',
    		'timestamp',
    		'date_display',
    		'timesince',
    		'parent',
    		'likes',
    		'did_like',
    		'reply',
    	]

    def get_did_like(self, obj):
    	request = self.context.get("request")
    	try:
    		user = request.user
    		if user.is_authenticated():
    			if user in obj.liked.all():
    				return True
    	except:
    		pass
    	return False

    def get_likes(self, obj):
    	return obj.liked.all().count()

    def get_date_display(self, obj):
    	return obj.timestamp.strftime("%b %d, %Y | at %I:%M %p")

    def get_timesince(self, obj):
    	return timesince(obj.timestamp) + " ago"