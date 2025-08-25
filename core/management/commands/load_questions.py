from django.core.management.base import BaseCommand
from core.models import Question

class Command(BaseCommand):
    help = 'Load default quiz questions into the database'

    def handle(self, *args, **kwargs):
        questions = [
            ("I enjoy solving complex problems and puzzles.", "Logical Reasoning"),
            ("I can easily identify patterns and relationships between ideas.", "Analytical Thinking"),
            ("I am confident when speaking in front of a group.", "Communication"),
            ("I can express my thoughts clearly in writing.", "Communication"),
            ("I often come up with original ideas or solutions.", "Creativity"),
            ("I enjoy working on creative projects like writing, design, or art.", "Creativity"),
            ("I feel comfortable taking the lead on a project or group task.", "Leadership"),
            ("I am good at motivating others to achieve a goal.", "Leadership"),
            ("I work well with others in a team setting.", "Teamwork"),
            ("I am good at resolving conflicts between people.", "Interpersonal Skills"),
            ("I manage my time effectively to meet deadlines.", "Time Management"),
            ("I keep things organized and plan ahead for tasks.", "Planning & Organization"),
            ("I am comfortable using technology to complete tasks or solve problems.", "Tech Skills"),
            ("I enjoy learning new things and picking up new skills quickly.", "Adaptability"),
            ("I stay calm and focused even when I’m under pressure.", "Emotional Intelligence"),
        ]

        for text, category in questions:
            Question.objects.get_or_create(text=text, category=category)

        self.stdout.write(self.style.SUCCESS("Questions loaded successfully."))
