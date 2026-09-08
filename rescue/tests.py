from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import AdoptionApplication, Animal, LostFound, RescueReport


class PawConnectFlowTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='helper', password='StrongPass123!')
		self.animal = Animal.objects.create(
			name='Milo', animal_type='Dog', age=2, gender='Male',
			description='Friendly and healthy.', location='Kathmandu', health_status='Healthy',
		)

	def test_registration_hashes_password_and_redirects_to_login(self):
		response = self.client.post(reverse('register'), {
			'first_name': 'New', 'last_name': 'Helper', 'username': 'newhelper',
			'email': 'new@example.com', 'password1': 'StrongPass123!abc',
			'password2': 'StrongPass123!abc',
		})
		self.assertRedirects(response, reverse('login'))
		created_user = User.objects.get(username='newhelper')
		self.assertTrue(created_user.has_usable_password())
		self.assertNotEqual(created_user.password, 'StrongPass123!abc')

	def test_dashboard_requires_login(self):
		response = self.client.get(reverse('dashboard'))
		self.assertRedirects(response, f'{reverse("login")}?next={reverse("dashboard")}')

	def test_dashboard_renders_rescue_name(self):
		RescueReport.objects.create(
			user=self.user,
			animal_name='Charlie',
			animal_type='Dog',
			description='Needs care.',
			location='Kathmandu',
			contact_number='555-0102',
		)
		self.client.force_login(self.user)
		response = self.client.get(reverse('dashboard'))
		self.assertContains(response, 'Charlie')
		self.assertNotContains(response, '{{ report.animal_name }}')

	def test_logged_in_user_can_submit_rescue_report(self):
		self.client.force_login(self.user)
		response = self.client.post(reverse('rescue'), {
			'animal_name': 'Injured dog', 'animal_type': 'Dog',
			'description': 'Needs help near the park.', 'location': 'Lalitpur',
			'contact_number': '555-0100',
		})
		self.assertRedirects(response, reverse('rescue'))
		self.assertTrue(RescueReport.objects.filter(user=self.user, animal_name='Injured dog').exists())

	def test_same_user_cannot_apply_twice(self):
		self.client.force_login(self.user)
		payload = {'message': 'I can provide a loving home.'}
		self.client.post(reverse('apply-to-adopt', args=[self.animal.id]), payload)
		response = self.client.get(reverse('apply-to-adopt', args=[self.animal.id]))
		self.assertRedirects(response, reverse('adopt'))
		self.assertEqual(AdoptionApplication.objects.filter(user=self.user, animal=self.animal).count(), 1)

	def test_public_pages_render(self):
		for route_name in ('home', 'rescue', 'adopt', 'lost-found', 'about'):
			with self.subTest(route_name=route_name):
				self.assertEqual(self.client.get(reverse(route_name)).status_code, 200)

	def test_auth_pages_render(self):
		self.assertEqual(self.client.get(reverse('login')).status_code, 200)
		self.assertEqual(self.client.get(reverse('register')).status_code, 200)

	def test_lost_found_renders_animal_name(self):
		LostFound.objects.create(
			user=self.user,
			report_type='Lost',
			animal_name='Luna',
			animal_type='Cat',
			description='Missing near the park.',
			location='Lalitpur',
			date_lost_found='2026-09-08',
			contact_number='555-0100',
		)
		response = self.client.get(reverse('lost-found'))
		self.assertContains(response, 'Luna')
		self.assertNotContains(response, '{{ report.animal_name }}')

	def test_rescue_renders_animal_name(self):
		RescueReport.objects.create(
			user=self.user,
			animal_name='Buddy',
			animal_type='Dog',
			description='Needs help near the road.',
			location='Kathmandu',
			contact_number='555-0101',
		)
		response = self.client.get(reverse('rescue'))
		self.assertContains(response, 'Buddy')
		self.assertNotContains(response, '{{ report.animal_name }}')
