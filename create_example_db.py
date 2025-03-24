import random
from datetime import date, timedelta

from sqlalchemy import func, select

from app import create_app
from models import *

app = create_app()

def generate_random_string(length=20):
    """Generates a random string of given length."""
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "
    return "".join(random.choice(characters) for _ in range(length))

def generate_random_date():
    """Generates a random date within a reasonable past range."""
    start_date = date.today() - timedelta(days=365) # Up to a year ago
    end_date = date.today()
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_number_of_days)

def generate_random_duration():
    """Generates a random quiz duration in minutes (optional, up to 120 minutes)."""
    return random.randint(15, 120) if random.random() < 0.7 else None # 70% chance of having duration

def generate_random_remarks():
    """Generates random remarks (optional)."""
    return generate_random_string(50) if random.random() < 0.5 else "" # 50% chance of remarks

def generate_random_subject():
    """Generates a random Subject instance."""
    return Subject(
        subject_name=f"Subject - {generate_random_string(10).strip()}",
        description=generate_random_string(50)
    )

def generate_random_chapter(subject: Subject):
    """Generates a random Chapter instance for a given Subject."""
    # since composite keys have to be incremented manually in sqlite
    max_number = db.session.scalar(
        select(func.max(Chapter.chapter_id)).where(Chapter.subject_id == subject.subject_id)
    )
    # If there are no chapters yet, max_number will be None. Start at 1.
    chapter_number = (max_number or 0) + 1

    return Chapter(
        subject_id=subject.subject_id,
        chapter_id=chapter_number,
        chapter_name=f"Chapter - {generate_random_string(10).strip()}",
        description=generate_random_string(50),
        subject=subject
    )

def generate_random_quiz(subject: Subject, chapter: Chapter):
    """Generates a random Quiz instance for a given Chapter and Subject."""
    return Quiz(
        quiz_name=f"Quiz - {generate_random_string(10).strip()}",
        chapter_id=chapter.chapter_id,
        subject_id=subject.subject_id,
        date=generate_random_date() if random.random() < 0.8 else None, # 80% chance of having a date
        duration=generate_random_duration(),
        remarks=generate_random_remarks(),
        chapter=chapter
    )

def generate_random_question(quiz: Quiz):
    """Generates a random Question instance for a given Quiz."""
    return Question(
        quiz_id=quiz.quiz_id,
        text=f"Question - {generate_random_string(30).strip()}?",
        marks=random.randint(1, 5),
        is_msq=random.random() < 0.3, # 30% chance of being MSQ
        quiz=quiz
)

def generate_random_option(question: Question, is_correct: bool):
    """Generates a random Option instance for a given Question."""
    return Option(
        question_id=question.question_id,
        text=f"Option - {generate_random_string(20).strip()}",
        is_correct=is_correct,
        question=question
    )

def populate_database(session, num_subjects=3, chapters_per_subject=2, quizzes_per_chapter=2, questions_per_quiz=5, options_per_question=4):
    """Populates the database with random data."""
    subjects = []
    for _ in range(num_subjects):
        subject = generate_random_subject()
        session.add(subject)
        subjects.append(subject)

    chapters = []
    for subject in subjects:
        for _ in range(chapters_per_subject):
            chapter = generate_random_chapter(subject)
            session.add(chapter)
            chapters.append(chapter)

    quizzes = []
    for chapter in chapters:
        for _ in range(quizzes_per_chapter):
            quiz = generate_random_quiz(chapter.subject, chapter)
            session.add(quiz)
            quizzes.append(quiz)

    questions_list = [] # to keep track of all questions for option generation later
    for quiz in quizzes:
        for _ in range(questions_per_quiz):
            question = generate_random_question(quiz)
            session.add(question)
            questions_list.append(question)

    for question in questions_list:
        correct_option_index = random.randint(0, options_per_question - 1) # Decide which option is correct
        for i in range(options_per_question):
            is_correct = (i == correct_option_index)
            option = generate_random_option(question, is_correct)
            session.add(option)

    session.commit()
    print("Database populated with random data.")

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
    
    populate_database(db.session)

    print("Dummy data created successfully!")

