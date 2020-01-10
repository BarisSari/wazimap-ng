from wazimap_ng.datasets.models import (
    Dataset,
    Indicator,
    IndicatorSubcategory,
    IndicatorCategory,
    Profile,
    ProfileIndicator,
)

from rest_framework import status
from rest_framework.reverse import reverse
from django.test import TestCase
from nose.tools import eq_
from faker import Faker

fake = Faker(seed=123456789)


class ProfileTestCase(TestCase):
    def setUp(self) -> None:
        self.first_dataset = Dataset.objects.create(name="first")
        self.first_profile = Profile.objects.create(name="first_profile")
        indicator = Indicator.objects.create(
            name="first_indicator",
            groups=["first_group"],
            label="first_label",
            dataset=self.first_dataset,
        )
        indicator_category = IndicatorCategory.objects.create(
            name="category_1",
            profile=self.first_profile,
        )
        indicator_subcategory = IndicatorSubcategory.objects.create(
            name="sub_category_1",
            category=indicator_category,
        )
        ProfileIndicator.objects.create(
            profile=self.first_profile,
            indicator=indicator,
            subcategory=indicator_subcategory,
        )
        self.second_profile = Profile.objects.create(name="second_profile")

    def tearDown(self) -> None:
        Dataset.objects.all().delete()
        Profile.objects.all().delete()
        Indicator.objects.all().delete()

    def test_correct_profile_list_returned(self):
        url = reverse("profile-list")
        response = self.client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]
        eq_(len(results), 2)
        eq_(results[0]["name"], "first_profile")
        eq_(results[1]["name"], "second_profile")

    def test_correct_profile_returned(self):
        pk = self.first_profile.pk
        url = reverse("profile-detail", kwargs={"pk": pk})
        response = self.client.get(url, format="json")
        eq_(response.status_code, status.HTTP_200_OK)

        results = response.data
        eq_(results["name"], "first_profile")
        eq_(results["indicators"][0]["subcategory"], "sub_category_1")
        eq_(results["indicators"][0]["category"], "category_1")
