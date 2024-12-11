import typing

from django.utils.translation import ugettext_lazy as _

import django.urls

import cms.menu_bases
from menus.base import Menu, NavigationNode
import menus.menu_pool
from pinogy_pet.pos_api import PetTypeList, APIPetTypeSetting
from pinogy_breeds.pos_api import BreedList, PetTypeList, Breed

class AvailablePetsMenu(cms.menu_bases.CMSAttachMenu):
    name = _('Available Pets Menu')

    def get_nodes(self, request):
        nodes = []
        pet_types = PetTypeList()
        pet_types_list = pet_types.get_pet_type_list(None)
        pet_types_filtered = []
        for pet_type in pet_types_list:
             if pet_type:
                name = pet_type.name
                title = name
                if pet_type.plurals:
                    title = pet_type.plurals.get(name, name)

                pet_types_filtered.append({
                    'id': pet_type.id,
                    'url': django.urls.reverse('pinogy_pet:pet_type', kwargs=dict(pet_type_slug=pet_type.slug)),
                    'title': title
                })

        if pet_types_filtered:  
            pet_types_filtered = sorted(pet_types_filtered, key=lambda item: item['title'])
            for item in pet_types_filtered:
                node = menus.base.NavigationNode(
                    title=item['title'],
                    url=item['url'],
                    id=item['id']
                )
                nodes.append(node)
        return nodes
menus.menu_pool.menu_pool.register_menu(AvailablePetsMenu)
