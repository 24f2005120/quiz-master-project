from app import create_app
import random
from models import *
app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(username="admin", password="password")
    db.session.add(admin)

    # Create Subjects
    math_subject = Subject(subject_name="Mathematics", description="The study of numbers, quantities, and space.")
    physics_subject = Subject(subject_name="Physics", description="The science of nature in the broadest sense.")
    chemistry_subject = Subject(subject_name="Chemistry", description="The science that deals with the composition, structure, and properties of substances and with the transformations that they undergo.")
    db.session.add_all([math_subject, physics_subject, chemistry_subject])
    db.session.flush() # Flush to get subject_id for chapters

    # Create Chapters for Math
    algebra_chapter = Chapter(subject_id=math_subject.subject_id, chapter_id=1, chapter_name="Algebra Basics", description="Introduction to algebraic concepts.")
    calculus_chapter = Chapter(subject_id=math_subject.subject_id, chapter_id=2, chapter_name="Calculus I", description="Basic differential and integral calculus.")
    db.session.add_all([algebra_chapter, calculus_chapter])
    db.session.flush() # Flush to get chapter_id for quizzes

    # Create Quizzes for Algebra
    algebra_quiz_1 = Quiz(subject_id=math_subject.subject_id, chapter_id=algebra_chapter.chapter_id, quiz_name="Algebra Quiz 1", remarks="Basic Algebra", duration=30)
    algebra_quiz_2 = Quiz(subject_id=math_subject.subject_id, chapter_id=algebra_chapter.chapter_id, quiz_name="Algebra Quiz 2", remarks="Intermediate Algebra", duration=45)
    db.session.add_all([algebra_quiz_1, algebra_quiz_2])
    db.session.flush() # Flush to get quiz_id for questions

    # Create Questions for Algebra Quiz 1 - Manual Questions
    q1_algebra_1 = Question(quiz_id=algebra_quiz_1.quiz_id, text="What is the value of x in the equation 2x + 5 = 11?", marks=2)
    q2_algebra_1 = Question(quiz_id=algebra_quiz_1.quiz_id, text="Simplify the expression: 3(a + 2b) - (a - b)", marks=3)
    db.session.add_all([q1_algebra_1, q2_algebra_1])
    db.session.flush() # Flush to get question_id for options

    # Create Options for Manual Questions
    # Question 1 options
    options_q1_algebra_1 = [
        Option(question_id=q1_algebra_1.question_id, text="x = 2", is_correct=False),
        Option(question_id=q1_algebra_1.question_id, text="x = 3", is_correct=True),
        Option(question_id=q1_algebra_1.question_id, text="x = 4", is_correct=False),
        Option(question_id=q1_algebra_1.question_id, text="x = 5", is_correct=False),
    ]
    # Question 2 options
    options_q2_algebra_1 = [
        Option(question_id=q2_algebra_1.question_id, text="2a + 5b", is_correct=True),
        Option(question_id=q2_algebra_1.question_id, text="2a + 7b", is_correct=False),
        Option(question_id=q2_algebra_1.question_id, text="4a + 5b", is_correct=False),
        Option(question_id=q2_algebra_1.question_id, text="4a + 7b", is_correct=False),
    ]
    db.session.add_all(options_q1_algebra_1 + options_q2_algebra_1)


    # Create Questions for Algebra Quiz 2 - Auto-generated Math Questions
    num_auto_questions = 5
    for i in range(num_auto_questions):
        num1 = random.randint(1, 20)
        num2 = random.randint(1, 20)
        operator = random.choice(['+', '-', '*'])
        if operator == '+':
            answer = num1 + num2
            question_text = f"What is {num1} + {num2}?"
        elif operator == '-':
            answer = num1 - num2
            question_text = f"What is {num1} - {num2}?"
        elif operator == '*':
            answer = num1 * num2
            question_text = f"What is {num1} * {num2}?"

        question = Question(quiz_id=algebra_quiz_2.quiz_id, text=question_text, marks=1)
        db.session.add(question)
        db.session.flush() # Get question_id to create options

        options = []
        correct_option = Option(question_id=question.question_id, text=str(answer), is_correct=True)
        options.append(correct_option)

        # Add incorrect options (simple variations around the answer)
        for _ in range(3):
            incorrect_answer = answer + random.randint(-3, 3)
            while str(incorrect_answer) in [opt.text for opt in options]: # Ensure unique incorrect options
                incorrect_answer = answer + random.randint(-3, 3)
            options.append(Option(question_id=question.question_id, text=str(incorrect_answer), is_correct=False))

        random.shuffle(options) # Shuffle options to randomize correct answer position
        db.session.add_all(options)


    db.session.commit()

    print("Dummy data created successfully!")

