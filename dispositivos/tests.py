from django.test import TestCase
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Device, Measurement, Category, Zone, Organization

class DeviceTestCase(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(name="Test Org", email="test@org.com")
        self.category = Category.objects.create(name="Test Category", organization=self.organization)
        self.zone = Zone.objects.create(name="Test Zone", organization=self.organization)
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        self.user.groups.add(Group.objects.create(name="Manager"))
        self.device = Device.objects.create(
            name="Test Device",
            category=self.category,
            zone=self.zone,
            organization=self.organization
        )

    def test_device_creation(self):
        self.assertEqual(self.device.name, "Test Device")
        self.assertEqual(self.device.organization.name, "Test Org")

    def test_device_list_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse('device_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dispositivos/device_list.html')

    def test_measurement_creation(self):
        measurement = Measurement.objects.create(
            device=self.device,
            value=25.5,
            unit="Celsius"
        )
        self.assertEqual(measurement.device.name, "Test Device")
        self.assertEqual(measurement.value, 25.5)
