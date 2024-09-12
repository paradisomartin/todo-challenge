from rest_framework import serializers
from .models import Task, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']
        read_only_fields = ['id']

class TaskSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'is_completed', 'tags']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        tags_data = self.context['request'].data.get('tags', [])
        task = Task.objects.create(user=self.context['request'].user, **validated_data)
        for tag_title in tags_data:
            tag, _ = Tag.objects.get_or_create(title=tag_title, user=task.user)
            task.tags.add(tag)
        return task

    def update(self, instance, validated_data):
        tags_data = self.context['request'].data.get('tags', None)
        instance = super().update(instance, validated_data)

        if tags_data is not None:
            instance.tags.clear()
            for tag_title in tags_data:
                tag, _ = Tag.objects.get_or_create(user=instance.user, title=tag_title)
                instance.tags.add(tag)

        return instance
