from rest_framework import serializers
from .models import Task, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']
        read_only_fields = ['id']

class TagListField(serializers.ListField):
    child = serializers.CharField()

class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    tag_titles = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'tags', 'tag_titles']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        if 'description' not in validated_data:
            validated_data['description'] = ''
        task = Task.objects.create(user=self.context['request'].user, **validated_data)
        for tag_title in tags_data:
            tag, _ = Tag.objects.get_or_create(title=tag_title, user=task.user)
            task.tags.add(tag)
        return task

    def get_tag_titles(self, obj):
        return [tag.title for tag in obj.tags.all()]

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tags', None)
        instance = super().update(instance, validated_data)

        if tag_names is not None:
            instance.tags.clear()
            for tag_name in tag_names:
                tag, _ = Tag.objects.get_or_create(user=instance.user, title=tag_name)
                instance.tags.add(tag)

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = [tag.title for tag in instance.tags.all()]
        return representation
