import random
from datetime import date, timedelta

from sqlalchemy import func, select

from app import create_app
from models.models import *

app = create_app()

def add_dummy_data():
    # Users
    user1 = User(username='user1', password='password1')
    user2 = User(username='user2', password='password2')
    db.session.add_all([user1, user2])
    db.session.commit()

    # Subjects
    subject1 = Subject(subject_name='Mathematics', description='The study of numbers, quantities, and space.')
    subject2 = Subject(subject_name='Science', description='The systematic study of the physical and natural world.')
    subject3 = Subject(subject_name='History', description='Study of past events.')
    subject4 = Subject(subject_name='Literature', description='Study of written works.')
    db.session.add_all([subject1, subject2, subject3, subject4])
    db.session.commit()

    # Chapters for Mathematics
    chapter1_math = Chapter(subject_id=subject1.subject_id, chapter_id=1, chapter_name='Algebra', description='Basic algebraic operations.')
    chapter2_math = Chapter(subject_id=subject1.subject_id, chapter_id=2, chapter_name='Geometry', description='Shapes and spatial relationships.')
    db.session.add_all([chapter1_math, chapter2_math])
    db.session.commit()

    # Chapters for Science
    chapter1_science = Chapter(subject_id=subject2.subject_id, chapter_id=1, chapter_name='Physics', description='The study of matter and energy.')
    chapter2_science = Chapter(subject_id=subject2.subject_id, chapter_id=2, chapter_name='Biology', description='The study of living organisms.')
    db.session.add_all([chapter1_science, chapter2_science])
    db.session.commit()

    # Chapters for History
    chapter1_history = Chapter(subject_id=subject3.subject_id, chapter_id=1, chapter_name='Ancient History', description='History of ancient civilizations.')
    chapter2_history = Chapter(subject_id=subject3.subject_id, chapter_id=2, chapter_name='Modern History', description='History from the 18th century onwards.')
    db.session.add_all([chapter1_history, chapter2_history])
    db.session.commit()

    # Chapters for Literature
    chapter1_literature = Chapter(subject_id=subject4.subject_id, chapter_id=1, chapter_name='Poetry', description='Study of poetic forms and movements.')
    chapter2_literature = Chapter(subject_id=subject4.subject_id, chapter_id=2, chapter_name='Drama', description='Study of plays and theatrical works.')
    db.session.add_all([chapter1_literature, chapter2_literature])
    db.session.commit()

    # Quizzes for Algebra (Mathematics)
    quiz1_algebra = Quiz(quiz_name='Algebra Basics Quiz', chapter_id=chapter1_math.chapter_id, subject_id=chapter1_math.subject_id, date=date(2025, 1, 20), duration=1, remarks='Basic algebra quiz', total_marks=20)
    quiz2_algebra = Quiz(quiz_name='Advanced Algebra Quiz', chapter_id=chapter1_math.chapter_id, subject_id=chapter1_math.subject_id, date=date(2025, 1, 25), duration=45, remarks='Advanced algebra quiz', total_marks=30)
    db.session.add_all([quiz1_algebra, quiz2_algebra])
    db.session.commit()

    # Quizzes for Geometry (Mathematics)
    quiz1_geometry = Quiz(quiz_name='Geometry Fundamentals', chapter_id=chapter2_math.chapter_id, subject_id=chapter2_math.subject_id, date=date(2025, 2, 1), duration=40, remarks='Basic geometry quiz', total_marks=25)
    db.session.add_all([quiz1_geometry])
    db.session.commit()

    # Quizzes for Physics (Science)
    quiz1_physics = Quiz(quiz_name='Newtonian Mechanics', chapter_id=chapter1_science.chapter_id, subject_id=chapter1_science.subject_id, date=date(2025, 2, 10), duration=35, remarks='Basic physics principles', total_marks=20)
    quiz2_physics = Quiz(quiz_name='Thermodynamics', chapter_id=chapter1_science.chapter_id, subject_id=chapter1_science.subject_id, date=date(2025, 2, 15), duration=50, remarks='Heat and energy transfer', total_marks=30)
    db.session.add_all([quiz1_physics, quiz2_physics])
    db.session.commit()

    # Quizzes for Biology (Science)
    quiz1_biology = Quiz(quiz_name='Cell Biology', chapter_id=chapter2_science.chapter_id, subject_id=chapter2_science.subject_id, date=date(2025, 2, 20), duration=40, remarks='Basic cell structures', total_marks=25)
    db.session.add_all([quiz1_biology])
    db.session.commit()

    # Quizzes for Ancient History (History)
    quiz1_ancient_history = Quiz(quiz_name='Ancient Egypt', chapter_id=chapter1_history.chapter_id, subject_id=chapter1_history.subject_id, date=date(2025, 3, 1), duration=45, remarks='Egyptian civilization', total_marks=30)
    db.session.add_all([quiz1_ancient_history])
    db.session.commit()

    # Quizzes for Modern History (History)
    quiz1_modern_history = Quiz(quiz_name='World War I', chapter_id=chapter2_history.chapter_id, subject_id=chapter2_history.subject_id, date=date(2025, 3, 10), duration=50, remarks='Causes and effects of WWI', total_marks=35)
    db.session.add_all([quiz1_modern_history])
    db.session.commit()

    # Quizzes for Poetry (Literature)
    quiz1_poetry = Quiz(quiz_name='Shakespearean Sonnets', chapter_id=chapter1_literature.chapter_id, subject_id=chapter1_literature.subject_id, date=date(2025, 3, 15), duration=40, remarks='Analysis of sonnets', total_marks=25)
    db.session.add_all([quiz1_poetry])
    db.session.commit()

    # Quizzes for Drama (Literature)
    quiz1_drama = Quiz(quiz_name='Hamlet', chapter_id=chapter2_literature.chapter_id, subject_id=chapter2_literature.subject_id, date=date(2025, 3, 20), duration=55, remarks='Shakespearean tragedy', total_marks=40)
    db.session.add_all([quiz1_drama])
    db.session.commit()


    # Questions for Algebra Basics Quiz (already present, keeping it)
    q1_algebra1 = Question(quiz_id=quiz1_algebra.quiz_id, text='What is 2 + 2?', marks=5)
    q2_algebra1 = Question(quiz_id=quiz1_algebra.quiz_id, text='Solve for x: x - 5 = 10', marks=5)
    q3_algebra1 = Question(quiz_id=quiz1_algebra.quiz_id, text='Simplify: 3y + 2y', marks=5)
    q4_algebra1 = Question(quiz_id=quiz1_algebra.quiz_id, text='What is 5 * 3?', marks=5)
    db.session.add_all([q1_algebra1, q2_algebra1, q3_algebra1, q4_algebra1])
    db.session.commit()
    quiz1_algebra.total_marks = sum(q.marks for q in quiz1_algebra.questions)
    db.session.commit()


    # Options for Question 1 of Algebra Basics Quiz (already present, keeping it)
    option1_q1_algebra1 = Option(question_id=q1_algebra1.question_id, text='3', is_correct=False)
    option2_q1_algebra1 = Option(question_id=q1_algebra1.question_id, text='4', is_correct=True)
    option3_q1_algebra1 = Option(question_id=q1_algebra1.question_id, text='5', is_correct=False)
    db.session.add_all([option1_q1_algebra1, option2_q1_algebra1, option3_q1_algebra1])
    db.session.commit()

    # Options for Question 2 of Algebra Basics Quiz (already present, keeping it)
    option1_q2_algebra1 = Option(question_id=q2_algebra1.question_id, text='5', is_correct=False)
    option2_q2_algebra1 = Option(question_id=q2_algebra1.question_id, text='10', is_correct=False)
    option3_q2_algebra1 = Option(question_id=q2_algebra1.question_id, text='15', is_correct=True)
    db.session.add_all([option1_q2_algebra1, option2_q2_algebra1, option3_q2_algebra1])
    db.session.commit()

    # Options for Question 3 of Algebra Basics Quiz (already present, keeping it)
    option1_q3_algebra1 = Option(question_id=q3_algebra1.question_id, text='4y', is_correct=False)
    option2_q3_algebra1 = Option(question_id=q3_algebra1.question_id, text='5y', is_correct=True)
    option3_q3_algebra1 = Option(question_id=q3_algebra1.question_id, text='6y', is_correct=False)
    db.session.add_all([option1_q3_algebra1, option2_q3_algebra1, option3_q3_algebra1])
    db.session.commit()

    # Options for Question 4 of Algebra Basics Quiz (already present, keeping it)
    option1_q4_algebra1 = Option(question_id=q4_algebra1.question_id, text='12', is_correct=False)
    option2_q4_algebra1 = Option(question_id=q4_algebra1.question_id, text='15', is_correct=True)
    option3_q4_algebra1 = Option(question_id=q4_algebra1.question_id, text='18', is_correct=False)
    db.session.add_all([option1_q4_algebra1, option2_q4_algebra1, option3_q4_algebra1])
    db.session.commit()

    # Questions for Newtonian Mechanics Quiz (Physics Quiz 1)
    q1_physics1 = Question(quiz_id=quiz1_physics.quiz_id, text='Newton\'s first law is also known as the law of?', marks=5)
    q2_physics1 = Question(quiz_id=quiz1_physics.quiz_id, text='What is the unit of force?', marks=5)
    db.session.add_all([q1_physics1, q2_physics1])
    db.session.commit()
    quiz1_physics.total_marks = sum(q.marks for q in quiz1_physics.questions)
    db.session.commit()

    # Options for Question 1 of Newtonian Mechanics Quiz
    option1_q1_physics1 = Option(question_id=q1_physics1.question_id, text='Acceleration', is_correct=False)
    option2_q1_physics1 = Option(question_id=q1_physics1.question_id, text='Inertia', is_correct=True)
    option3_q1_physics1 = Option(question_id=q1_physics1.question_id, text='Gravity', is_correct=False)
    db.session.add_all([option1_q1_physics1, option2_q1_physics1, option3_q1_physics1])
    db.session.commit()

    # Options for Question 2 of Newtonian Mechanics Quiz
    option1_q2_physics1 = Option(question_id=q2_physics1.question_id, text='Watt', is_correct=False)
    option2_q2_physics1 = Option(question_id=q2_physics1.question_id, text='Joule', is_correct=False)
    option3_q2_physics1 = Option(question_id=q2_physics1.question_id, text='Newton', is_correct=True)
    db.session.add_all([option1_q2_physics1, option2_q2_physics1, option3_q2_physics1])
    db.session.commit()


    # Quiz Attempts for user1 on Algebra Basics Quiz (already present, keeping it)
    attempt1_user1_quiz1 = QuizAttempt(
        quiz_id=quiz1_algebra.quiz_id,
        user_id=user1.user_id,
        start_time=datetime.now(),
        time_taken=25,
        total_score=15,
        percentage=75.0  # (15/20) * 100
    )
    db.session.add(attempt1_user1_quiz1)
    db.session.commit()

    # Question Attempts for attempt1_user1_quiz1 (already present, keeping it)
    qa1_attempt1 = QuestionAttempt(quiz_attempt_id=attempt1_user1_quiz1.id, question_id=q1_algebra1.question_id, marks_gained=5, selected_options=[option2_q1_algebra1]) # Correct option selected
    qa2_attempt1 = QuestionAttempt(quiz_attempt_id=attempt1_user1_quiz1.id, question_id=q2_algebra1.question_id, marks_gained=5, selected_options=[option3_q2_algebra1]) # Correct option selected
    qa3_attempt1 = QuestionAttempt(quiz_attempt_id=attempt1_user1_quiz1.id, question_id=q3_algebra1.question_id, marks_gained=5, selected_options=[option2_q3_algebra1]) # Correct option selected
    qa4_attempt1 = QuestionAttempt(quiz_attempt_id=attempt1_user1_quiz1.id, question_id=q4_algebra1.question_id, marks_gained=0, selected_options=[option1_q4_algebra1]) # Incorrect option selected
    db.session.add_all([qa1_attempt1, qa2_attempt1, qa3_attempt1, qa4_attempt1])
    db.session.commit()

    attempt1_user2_quiz1 = QuizAttempt(
        quiz_id=quiz1_algebra.quiz_id,
        user_id=user2.user_id,
        start_time=datetime.now(),
        time_taken=35,
        total_score=18,
        percentage=90.0
    )
    db.session.add(attempt1_user2_quiz1)
    db.session.commit()

    # Question Attempts for attempt1_user2_quiz1 (example - user2 got all correct except q4)
    qa1_attempt1_u2 = QuestionAttempt(quiz_attempt_id=attempt1_user2_quiz1.id, question_id=q1_algebra1.question_id, marks_gained=5, selected_options=[option2_q1_algebra1])
    qa2_attempt1_u2 = QuestionAttempt(quiz_attempt_id=attempt1_user2_quiz1.id, question_id=q2_algebra1.question_id, marks_gained=5, selected_options=[option3_q2_algebra1])
    qa3_attempt1_u2 = QuestionAttempt(quiz_attempt_id=attempt1_user2_quiz1.id, question_id=q3_algebra1.question_id, marks_gained=5, selected_options=[option2_q3_algebra1])
    qa4_attempt1_u2 = QuestionAttempt(quiz_attempt_id=attempt1_user2_quiz1.id, question_id=q4_algebra1.question_id, marks_gained=3, selected_options=[option3_q4_algebra1]) # Incorrect option selected, partial marks if applicable in your system
    db.session.add_all([qa1_attempt1_u2, qa2_attempt1_u2, qa3_attempt1_u2, qa4_attempt1_u2])
    db.session.commit()


    # Quiz Attempts for user1 on Newtonian Mechanics Quiz (Physics Quiz 1)
    attempt1_user1_quiz_physics1 = QuizAttempt(
        quiz_id=quiz1_physics.quiz_id,
        user_id=user1.user_id,
        start_time=datetime.now(),
        time_taken=30,
        total_score=8, # out of 10
        percentage=80.0
    )
    db.session.add(attempt1_user1_quiz_physics1)
    db.session.commit()

    # Question Attempts for attempt1_user1_quiz_physics1
    qa1_attempt_physics1 = QuestionAttempt(quiz_attempt_id=attempt1_user1_quiz_physics1.id, question_id=q1_physics1.question_id, marks_gained=5, selected_options=[option2_q1_physics1]) # Correct
    qa2_attempt_physics1 = QuestionAttempt(quiz_attempt_id=attempt1_user1_quiz_physics1.id, question_id=q2_physics1.question_id, marks_gained=3, selected_options=[option1_q2_physics1]) # Incorrect
    db.session.add_all([qa1_attempt_physics1, qa2_attempt_physics1])
    db.session.commit()


    # Quiz Attempts for user2 on Cell Biology Quiz (Biology Quiz 1)
    attempt1_user2_quiz_biology1 = QuizAttempt(
        quiz_id=quiz1_biology.quiz_id,
        user_id=user2.user_id,
        start_time=datetime.now(),
        time_taken=38,
        total_score=20, # assuming quiz1_biology has total marks of 25, adjust if needed
        percentage=80.0
    )
    db.session.add(attempt1_user2_quiz_biology1)
    db.session.commit()

    # Assuming you add questions and options for quiz1_biology, you'd add QuestionAttempts here similarly
    # Example -  (replace q1_biology1, optionX_q1_biology1 with actual Question and Option objects)
    # qa1_attempt_biology1 = QuestionAttempt(quiz_attempt_id=attempt1_user2_quiz_biology1.id, question_id=q1_biology1.question_id, marks_gained=5, selected_options=[option2_q1_biology1])
    # db.session.add(qa1_attempt_biology1)
    # db.session.commit()


    # Quiz Attempts for user1 on Ancient Egypt Quiz (History Quiz 1)
    attempt1_user1_quiz_history1 = QuizAttempt(
        quiz_id=quiz1_ancient_history.quiz_id,
        user_id=user1.user_id,
        start_time=datetime.now(),
        time_taken=42,
        total_score=25, # assuming quiz1_ancient_history has total marks of 30
        percentage=83.33
    )
    db.session.add(attempt1_user1_quiz_history1)
    db.session.commit()
    # ... Add QuestionAttempts for History Quiz similarly if you add questions for it

    # Quiz Attempts for user2 on Shakespearean Sonnets Quiz (Literature Quiz 1)
    attempt1_user2_quiz_literature1 = QuizAttempt(
        quiz_id=quiz1_poetry.quiz_id,
        user_id=user2.user_id,
        start_time=datetime.now(),
        time_taken=35,
        total_score=18, # assuming quiz1_poetry has total marks of 25
        percentage=72.0
    )
    db.session.add(attempt1_user2_quiz_literature1)
    db.session.commit()

    print("Dummy data added successfully for all subjects!")

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(username="admin", password="password")
    db.session.add(admin)
    db.session.commit()
    add_dummy_data()

    print("Dummy data created successfully!")
