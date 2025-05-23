from django.http import HttpRequest
from django.test import TestCase

from lists.models import Item
from lists.views import home_page


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "home.html")

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST["item_text"] = "Nowy element listy"

        home_page(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "Nowy element listy")

    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST["item_text"] = "Nowy element listy"

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["location"], "/")

    def test_home_page_only_saves_items_when_necessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)

    def test_home_page_displays_all_list_items(self):
        Item.objects.create(text="itemik 1")
        Item.objects.create(text="itemik 2")

        request = HttpRequest()
        response = home_page(request)

        self.assertIn("itemik 1", response.content.decode())
        self.assertIn("itemik 2", response.content.decode())


class ItemModelTest(TestCase):

    def test_saving_retrieving_items(self):
        first_item = Item()
        first_item.text = "Absolutnie pierwszy element listy"
        first_item.save()

        second_item = Item()
        second_item.text = "Drugi element"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item, second_saved_item = saved_items
        self.assertEqual(first_saved_item.text, "Absolutnie pierwszy element listy")
        self.assertEqual(second_saved_item.text, "Drugi element")
