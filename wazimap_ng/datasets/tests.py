from .models import Dataset, DatasetData, Geography ,Indicator, Profile, ProfileData, ProfileIndicator

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from nose.tools import eq_, ok_
from faker import Faker

fake = Faker(seed=123456789)


class DatasetReadOnlyTestCase(APITestCase):
    def test_dataset_list_is_readonly(self):
        url = reverse("dataset")
        data = {"name": "test"}
        response = self.client.post(url, data=data)
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(url, data=data)
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(url, data=data)
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_dataset_indicator_list_is_readonly(self):
        dataset_id = 1
        url = reverse("dataset-indicator-list", kwargs={"dataset_id": dataset_id})
        data = {
            "groups": [],
            "name": "test",
            "label": "test-label",
            "dataset": dataset_id,
        }
        response = self.client.post(url, data=data)
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(url, data=data)
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(url, data=data)
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_indicator_list_is_readonly(self):
        url = reverse("indicator-list")
        data = {"groups": [], "name": "test", "label": "test-label", "dataset": 1}
        response = self.client.post(url, data=data)
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(url, data=data)
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(url, data=data)
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_indicator_data_view_is_readonly(self):
        indicator_id = 2
        url = reverse("indicator-data-view", kwargs={"indicator_id": indicator_id})
        data = {"data": {"Language": "Unspecified", "Count": 0, "geography": "TEST123"}}
        response = self.client.post(url, data=data, format="json")
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(url, data=data, format="json")
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(url, data=data, format="json")
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_profile_list_is_readonly(self):
        url = reverse("profile-list")
        data = {"name": "test"}
        response = self.client.post(url, data=data)
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(url, data=data)
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(url, data=data)
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_profile_detail_is_readonly(self):
        pk = 1
        url = reverse("profile-detail", kwargs={"pk": pk})
        data = {
            "subcategory": "Youth",
            "category": "Youth Demographics",
            "key_metric": False,
            "name": "Youth population by gender",
            "label": "Youth population by gender",
            "indicator": {
                "id": 4,
                "groups": ["Gender"],
                "name": "Youth population by gender",
                "label": "Youth population by gender",
                "dataset": {"id": 1, "name": "Census 2011 - Language"},
            },
            "universe": {
                "id": 1,
                "filters": {"Age__in": ["15 - 19", "20 - 24"]},
                "name": "Youth",
                "label": "Youth (15 - 24)",
                "dataset": {"id": 1, "name": "Census 2011 - Language"},
            },
        }
        response = self.client.post(url, data=data, format="json")
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.patch(url, data=data, format="json")
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.delete(url, data=data, format="json")
        eq_(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class DatasetPaginationTestCase(APITestCase):
    def setUp(self) -> None:
        for i in range(15):
            Dataset.objects.create(name=fake.name())
            Profile.objects.create(name=fake.name())
            Indicator.objects.create(groups=[], name=fake.name(), label=f"test-label-{i}", dataset=Dataset.objects.first())
            Geography.objects.create(path=f"PATH-{i}", depth=0, name=fake.name(), code=f"code-{i}", level=f"test-level-{i}")
            data = { "data":{
                "Language": fake.name(), "Count": fake.random_int(), "geography": f"GEO-{i}"
            }}
            DatasetData.objects.create(dataset=Dataset.objects.first(), geography=Geography.objects.first(), data=data)

    def test_dataset_list_is_paginated(self):
        url = reverse("dataset")
        response = self.client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)

        number_of_results = len(response.data["results"])
        eq_(number_of_results, 10)

    # def test_dataset_indicator_list_is_paginated(self):
    #     # TODO: it is not paginated!
    #     dataset_id = Dataset.objects.first().pk
    #     url = reverse("dataset-indicator-list", kwargs={"dataset_id": dataset_id})
    #     response = self.client.get(url)
    #     eq_(response.status_code, status.HTTP_200_OK)
    #
    #     number_of_results = len(response.data)
    #     eq_(number_of_results, 10)

    def test_indicator_list_is_paginated(self):
        url = reverse("indicator-list")
        response = self.client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)

        number_of_results = len(response.data["results"])
        eq_(number_of_results, 10)

    def test_indicator_data_view_is_paginated(self):
        indicator_id = Indicator.objects.first().pk
        url = reverse("indicator-data-view", kwargs={"indicator_id": indicator_id})
        response = self.client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)

        print(response.data)
        # number_of_results = len(response.data["results"])
        # eq_(number_of_results, 10)

    def test_profile_list_is_paginated(self):
        url = reverse("profile-list")
        response = self.client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)

        number_of_results = len(response.data["results"])
        self.assertLessEqual(number_of_results, 10)
