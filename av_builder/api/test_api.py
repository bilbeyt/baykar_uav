from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from aircrafts.models import Aircraft, AircraftModel, AircraftPart, AircraftPartName


class ApiTests(APITestCase):
    fixtures = ["data.json"]

    def setUp(self):
        self.client = APIClient()
        self.password = "baykar123456"

    def create_parts(self, model):
        for part_name in AircraftPartName:
            AircraftPart.objects.create(name=part_name, model=model)

    def test_assembly_team(self):
        self.create_parts(AircraftModel.AKINCI)
        self.client.login(username="assembly_user", password=self.password)
        url = reverse("list-create-aircrafts")
        data = {"model": AircraftModel.AKINCI}
        res = self.client.post(url, data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Aircraft.objects.filter(model=AircraftModel.AKINCI).count(), 1)

    def test_assembly_team_missing_parts(self):
        self.create_parts(AircraftModel.AKINCI)
        AircraftPart.objects.filter(
            model=AircraftModel.AKINCI, name=AircraftPartName.WING
        ).delete()
        self.client.login(username="assembly_user", password=self.password)
        url = reverse("list-create-aircrafts")
        data = {"model": AircraftModel.AKINCI}
        res = self.client.post(url, data, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            f"{AircraftPartName.WING} is missing for {AircraftModel.AKINCI}", res.json()[0]
        )
        self.assertEqual(Aircraft.objects.filter(model=AircraftModel.AKINCI).count(), 0)

    def test_other_teams(self):
        url = reverse("list-create-aircraft-parts")
        for name in AircraftPartName:
            self.client.login(username=name.lower() + "_user", password=self.password)
            data = {"model": AircraftModel.AKINCI, "name": name}
            res = self.client.post(url, data, format="json")
            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            self.assertEqual(
                AircraftPart.objects.filter(model=AircraftModel.AKINCI, name=name).count(), 1
            )

    def test_other_teams_forbidden(self):
        url = reverse("list-create-aircraft-parts")
        self.client.login(username="fuselage_user", password=self.password)
        data = {"model": AircraftModel.AKINCI, "name": AircraftPartName.AVIONICS}
        res = self.client.post(url, data, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            AircraftPart.objects.filter(
                model=AircraftModel.AKINCI, name=AircraftPartName.AVIONICS
            ).count(),
            0,
        )

    def test_part_delete(self):
        self.client.login(username="fuselage_user", password=self.password)
        obj = AircraftPart.objects.create(
            model=AircraftModel.AKINCI, name=AircraftPartName.FUSELAGE
        )
        url = reverse("destroy-aircraft-parts", args=[obj.id])
        res = self.client.delete(url, format="json")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            AircraftPart.objects.filter(
                model=AircraftModel.AKINCI, name=AircraftPartName.FUSELAGE
            ).count(),
            0,
        )

    def test_part_delete_other_teams(self):
        self.client.login(username="avionics_user", password=self.password)
        obj = AircraftPart.objects.create(
            model=AircraftModel.AKINCI, name=AircraftPartName.FUSELAGE
        )
        url = reverse("destroy-aircraft-parts", args=[obj.id])
        res = self.client.delete(url, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_part_delete_with_aircraft(self):
        self.client.login(username="fuselage_user", password=self.password)
        aircraft = Aircraft.objects.create(model=AircraftModel.AKINCI)
        obj = AircraftPart.objects.create(
            model=AircraftModel.AKINCI, name=AircraftPartName.FUSELAGE, aircraft=aircraft
        )
        url = reverse("destroy-aircraft-parts", args=[obj.id])
        res = self.client.delete(url, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            AircraftPart.objects.filter(
                model=AircraftModel.AKINCI, name=AircraftPartName.FUSELAGE
            ).count(),
            1,
        )
        self.assertEqual(Aircraft.objects.filter(model=AircraftModel.AKINCI).count(), 1)

    def test_delete_aircraft(self):
        self.client.login(username="assembly_user", password=self.password)
        aircraft = Aircraft.objects.create(model=AircraftModel.AKINCI)
        url = reverse("destroy-aircrafts", args=[aircraft.id])
        res = self.client.delete(url, format="json")
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Aircraft.objects.filter(model=AircraftModel.AKINCI).count(), 0)

    def test_delete_aircraft_other_teams(self):
        self.client.login(username="fuselage_user", password=self.password)
        aircraft = Aircraft.objects.create(model=AircraftModel.AKINCI)
        url = reverse("destroy-aircrafts", args=[aircraft.id])
        res = self.client.delete(url, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_part(self):
        self.client.login(username="fuselage_user", password=self.password)
        AircraftPart.objects.create(model=AircraftModel.AKINCI, name=AircraftPartName.FUSELAGE)
        url = reverse("list-create-aircraft-parts")
        res = self.client.get(url, format="datatable")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()["count"], 1)

    def test_list_part_from_other_teams(self):
        self.client.login(username="fuselage_user", password=self.password)
        AircraftPart.objects.create(model=AircraftModel.AKINCI, name=AircraftPartName.AVIONICS)
        url = reverse("list-create-aircraft-parts")
        res = self.client.get(url, format="datatable")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()["count"], 0)

    def test_list_aircrafts(self):
        self.client.login(username="assembly_user", password=self.password)
        Aircraft.objects.create(model=AircraftModel.AKINCI)
        url = reverse("list-create-aircrafts")
        res = self.client.get(url, format="datatable")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.json()["count"], 1)

    def test_list_aircrafts_with_other_teams(self):
        self.client.login(username="fuselage_user", password=self.password)
        Aircraft.objects.create(model=AircraftModel.AKINCI)
        url = reverse("list-create-aircrafts")
        res = self.client.get(url, format="datatable")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
