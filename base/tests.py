from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import Count
from .models import Member
from .models import MemberForm
from django.core.exceptions import ObjectDoesNotExist

class MemberListViewTest(TestCase):
    def test_member_list_view(self):
        response = self.client.get(reverse('members'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/member_list.html')
        self.assertQuerysetEqual(
            response.context['members'], 
            Member.objects.filter(b="0000000").order_by('created_at'), 
            transform=lambda x: x
        )
        self.assertEqual(response.context['count'], Member.objects.filter(b="0000000").count())

class MemberDetailViewTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create(first="John", last="Doe", number="555-1234", email="john@example.com", role="admin")

    def test_member_detail_view(self):
        response = self.client.get(reverse('member', args=[self.member.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/member.html')
        self.assertEqual(response.context['member'], self.member)

class MemberCreateViewTest(TestCase):
    def test_member_create_view(self):
        response = self.client.get(reverse('member-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/member_form.html')
        form = response.context['form']
        self.assertIsInstance(form, MemberForm)

        data = {'first': 'John', 'last': 'Doe', 'number': '555-1234', 'email': 'john@example.com', 'role': 'admin'}
        response = self.client.post(reverse('member-create'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('members'))
        self.assertEqual(Member.objects.count(), 1)

class MemberEditViewTest(TestCase):
    def setUp(self):
        self.member = Member.objects.create(first="John", last="Doe", number="555-1234", email="john@example.com", role="admin")

    def test_member_update_view(self):
        response = self.client.get(reverse('member-edit', args=[self.member.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base/member_edit.html')
        form = response.context['form']
        self.assertIsInstance(form, MemberForm)
        self.assertEqual(form.instance, self.member)

        data = {'first': 'Jane', 'last': 'Doe', 'number': '555-5678', 'email': 'jane@example.com', 'role': 'regular'}
        response = self.client.post(reverse('member-edit', args=[self.member.id]), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('members'))
        self.member.refresh_from_db()
        self.assertEqual(self.member.first, 'Jane')
        self.assertEqual(self.member.last, 'Doe')
        self.assertEqual(self.member.number, '555-5678')
        self.assertEqual(self.member.email, 'jane@example.com')
        self.assertEqual(self.member.role, 'regular')


class DeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.member = Member.objects.create(
            first="John",
            last="Smith",
            b="0000000",
            email="john@example.com",
            number="123-456-789",
        )
        self.delete_url = reverse('member-delete', args=[self.member.pk])

    def test_delete_member(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, 302)  # redirect status code
        with self.assertRaises(ObjectDoesNotExist):
            Member.objects.get(pk=self.member.pk)

    def test_delete_member_with_invalid_id(self):
        invalid_url = reverse('member-delete', args=[1000])
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, 404)  # not found status code

