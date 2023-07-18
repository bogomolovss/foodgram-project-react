from django.contrib import admin
from recipes.models import Favorite, Follow, Recipe, ShoppingCart


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    list_filter = ('author', 'name', 'tags')

    def count_favorites(self, obj):
        return obj.favorites.count()


admin.site.register(ShoppingCart)
admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(Recipe, RecipeAdmin)
