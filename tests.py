import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_question_default_points_and_max_selections():
    question = Question(title='q1')
    assert question.points == 1
    assert question.max_selections == 1

def test_create_question_with_invalid_points_below_range():
    with pytest.raises(Exception):
        Question(title='q1', points=0)

def test_create_question_with_invalid_points_above_range():
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_add_multiple_choices_and_validate_ids():
    question = Question(title='q1')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    assert choice1.id == 1
    assert choice2.id == 2
    assert len(question.choices) == 2

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice = question.add_choice('a')
    question.remove_choice_by_id(choice.id)
    assert len(question.choices) == 0

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_select_correct_choices():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('a')
    c2 = question.add_choice('b', is_correct=True)
    c3 = question.add_choice('c', is_correct=True)
    
    selected = question.select_choices([c2.id, c3.id])
    
    assert selected == [c2.id, c3.id]


def test_select_choices_raises_if_exceeds_max():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('a', is_correct=True)
    c2 = question.add_choice('b', is_correct=True)
    with pytest.raises(Exception):
        question.select_choices([c1.id, c2.id])

def test_set_correct_choices_behavior():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    question.set_correct_choices([c1.id])
    assert c1.is_correct
    assert not c2.is_correct

def test_add_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')
    with pytest.raises(Exception):
        question.add_choice('a' * 101)