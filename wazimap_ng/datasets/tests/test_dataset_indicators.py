from wazimap_ng.datasets.models import (
    Dataset,
    Indicator,
)

from rest_framework import status
from rest_framework.reverse import reverse
from django.test import TestCase
from nose.tools import eq_
from faker import Faker

fake = Faker(seed=123456789)


class DatasetIndicatorsTestCase(TestCase):
    def setUp(self) -> None:
        self.first_dataset = Dataset.objects.create(name="first")
        self.second_dataset = Dataset.objects.create(name="second")
        self.first_indicator = Indicator.objects.create(
            name="first_indicator",
            groups=["first_group"],
            label="first_label",
            dataset=self.first_dataset,
        )
        self.second_indicator = Indicator.objects.create(
            name="second_indicator",
            groups=["second_group"],
            label="second_label",
            dataset=self.second_dataset,
        )

    def test_all_dataset_returned(self):
        url = reverse("dataset")
        response = self.client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]
        number_of_results = response.data["count"]
        eq_(number_of_results, 2)
        eq_(results[0]["name"], "first")
        eq_(results[1]["name"], "second")

    def test_correct_dataset_returned(self):
        dataset_id = self.first_dataset.pk
        url = reverse("dataset-indicator-list", kwargs={"dataset_id": dataset_id})
        response = self.client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)

        result = response.data[0]
        eq_(result["dataset"], self.first_dataset.pk)

    def test_correct_indicators_returned(self):
        dataset_id = self.first_dataset.pk
        url = reverse("dataset-indicator-list", kwargs={"dataset_id": dataset_id})
        response = self.client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)

        result = response.data[0]
        eq_(result["groups"], ["first_group"])
        eq_(result["name"], "first_indicator")
        eq_(result["label"], "first_label")

    def test_incorrect_dataset_fails(self):
        # TODO: it returns empty instead of failing
        dataset_id = 123456789
        url = reverse("dataset-indicator-list", kwargs={"dataset_id": dataset_id})
        response = self.client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)

        number_of_results = len(response.data)
        eq_(number_of_results, 0)

    def test_all_indicators_return(self):
        url = reverse("indicator-list")
        response = self.client.get(url)
        eq_(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]
        number_of_results = response.data["count"]
        eq_(number_of_results, 2)
        eq_(results[0]["dataset"], self.first_dataset.pk)
        eq_(results[1]["dataset"], self.second_dataset.pk)
