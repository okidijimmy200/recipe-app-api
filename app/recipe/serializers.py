from django.db.models.query import QuerySet
from rest_framework import serializers

from core.models import Recipe, Tag, Ingredient

class TagSerializer(serializers.ModelSerializer):
    '''Serializer for tag objects'''

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)

class IngredientSerializer(serializers.ModelSerializer):
    '''Serializer for ingredient serializer'''

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)

# create serializer recipe serializer
class RecipeSerializer(serializers.ModelSerializer):
    '''serialize a recipe'''
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        # list fields to return
        fields = ('id', 'title', 'ingredients', 'tags', 'time_minutes', 'price', 'link')
        read_only_fields = ('id',)

class RecipeDetailSerializer(RecipeSerializer):
    '''Serialize a recipe detail'''
    # override the ingredients field
    ingredients = IngredientSerializer(many=True, read_only=True )
    tags = TagSerializer(many=True, read_only=True)

class RecipeImageSerializer(serializers.ModelSerializer):
    '''serializer for uploading images to recipes'''
    
    class Meta:
        model = Recipe
        fields = ('id', 'image')
        read_only_fields = ('id',)