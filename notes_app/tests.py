from django.test import TestCase
from django.urls import reverse
from .models import Note


class NoteModelTest(TestCase):
    def setUp(self):
        self.note = Note.objects.create(
            title="Sample Note",
            content="This is a sample note."
        )

    def test_note_creation(self):
        self.assertEqual(self.note.title, "Sample Note")
        self.assertEqual(self.note.content, "This is a sample note.")
        self.assertTrue(isinstance(self.note, Note))
        self.assertEqual(str(self.note), "Sample Note")


class NoteViewsTest(TestCase):
    def setUp(self):
        self.note = Note.objects.create(
            title="View Note",
            content="Note for testing views"
        )

    def test_note_list_view(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "View Note")
        self.assertTemplateUsed(response, "notes_app/note_list.html")

    def test_note_create_view(self):
        response = self.client.post(reverse("note_create"), {
            "title": "New Note",
            "content": "Created via test"
        })
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Note.objects.last().title, "New Note")

    def test_note_update_view(self):
        response = self.client.post(reverse("note_update", args=[self.note.id]), {
            "title": "Updated Title",
            "content": "Updated content"
        })
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Title")

    def test_note_delete_view(self):
        response = self.client.post(reverse("note_delete", args=[self.note.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
