import sys, random, threading, time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QButtonGroup, QRadioButton, QAbstractButton
from PyQt6.QtCore import pyqtSlot
import PyQt6.QtCore as QtCore

class QuizGame(QWidget):
    def __init__(self, questions, answers, questions_right_answers):
        super().__init__()

        self.questions = questions
        self.answers = answers
        self.questions_right_answers = questions_right_answers
        self.current_question = 0
        self.answer_selected = None
        self.score = 0

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1300, 300)
        self.setWindowTitle('Quiz Game')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.countdown_display = QLabel('20')
        self.countdown_display.setStyleSheet("font-size: 17px; font-weight: bold; line-height: 7px; margin: 0;")
        self.countdown_display.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.layout.addWidget(self.countdown_display)

        self.question_label = QLabel(self.questions[self.current_question])
        self.layout.addWidget(self.question_label)

        self.answer_buttons = []
        self.button_group = QButtonGroup()
        for i, answer in enumerate(self.answers[self.current_question]):
            button = QRadioButton(answer)
            self.button_group.addButton(button, i)
            self.answer_buttons.append(button)
            self.layout.addWidget(button)

        self.button_group.buttonToggled.connect(self.select_answer)

        self.confirm_button = QPushButton('Confirm')
        self.confirm_button.clicked.connect(self.check_answer)
        self.layout.addWidget(self.confirm_button)

        def update_timer():
            while True:
                self.decrease_timer()
                time.sleep(1)

        # Create a thread that calls the update_timer function
        timer_thread = threading.Thread(target=update_timer)
        timer_thread.daemon = True  # Set as daemon thread so it exits when main thread exits

        # Start the timer thread
        timer_thread.start()

    @pyqtSlot(QAbstractButton, bool)
    def select_answer(self, button, checked):
        if checked:
            self.answer_selected = self.button_group.id(button)

    @pyqtSlot()
    def check_answer(self):
        if self.answer_selected is not None:
            correct_answer_index = self.questions_right_answers[self.current_question]
            if self.answer_selected == correct_answer_index:
                self.score += 1
                self.answer_buttons[self.answer_selected].setStyleSheet('background-color: rgb(54, 189, 0)')
            else:
                self.answer_buttons[self.answer_selected].setStyleSheet('background-color: lightcoral')
                self.answer_buttons[correct_answer_index].setStyleSheet('background-color: rgb(54, 189, 0)')
            self.confirm_button.setText('Next')
            self.confirm_button.clicked.disconnect(self.check_answer)
            self.confirm_button.clicked.connect(self.next_question)
            return True # = there is an answer selected
        else:
            print("No answer selected")
            return False # = no answer is selected

    @pyqtSlot()
    def next_question(self):
        self.countdown_display.setStyleSheet('font-size: 17px; font-weight: bold; line-height: 7px; margin: 0; color: white')
        self.countdown_display.setText('20')
        def update_timer():
            while True:
                self.decrease_timer()
                time.sleep(1)
        # Create a thread that calls the update_timer function
        timer_thread = threading.Thread(target=update_timer)
        timer_thread.daemon = True  # Set as daemon thread so it exits when main thread exits
        # Start the timer thread
        timer_thread.start()
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.question_label.setText(self.questions[self.current_question])
            for button in self.answer_buttons:
                self.layout.removeWidget(button)
                button.deleteLater()
            self.answer_buttons = []
            self.button_group = QButtonGroup()
            for i, answer in enumerate(self.answers[self.current_question]):
                button = QRadioButton(answer)
                self.button_group.addButton(button, i)
                self.answer_buttons.append(button)
                self.layout.addWidget(button)
            self.layout.removeWidget(self.confirm_button)
            self.layout.addWidget(self.confirm_button)
            self.button_group.buttonToggled.connect(self.select_answer)
            self.confirm_button.setText('Confirm')
            self.confirm_button.clicked.disconnect(self.next_question)
            self.confirm_button.clicked.connect(self.check_answer)
        else:
            print("Quiz finished")
            print("Your score was: " + str(self.score) + "/" + str(len(self.questions)))
            self.close()

    @pyqtSlot()
    def decrease_timer(self):
        current_ = int(self.countdown_display.text())
        if current_ > 0:
            current_ -= 1
            self.countdown_display.setText(str(current_))
            if current_ == 0:
                self.countdown_display.setStyleSheet('font-size: 17px; font-weight: bold; line-height: 7px; margin: 0; color: red')
        else:
            status_ = self.check_answer()
            if status_ == False:
                self.confirm_button.setText('Next')
                #self.confirm_button.clicked.disconnect(self.check_answer)
                self.confirm_button.clicked.connect(self.next_question)

def shuffle_questions_with_answers(questions, answers, questions_right_answers):
    q_a = list(zip(questions, answers, questions_right_answers))
    random.shuffle(q_a)
    questions, answers, questions_right_answers = zip(*q_a)
    return list(questions), list(answers), list(questions_right_answers)

def shuffle_answer_order(answers, questions_right_answers, index_):
    text_of_correct_answer = answers[questions_right_answers[index_]]
    random.shuffle(answers)
    for i, answer in enumerate(answers):
        if answer == text_of_correct_answer:
            questions_right_answers[index_] = i
            break
    return answers, questions_right_answers[index_]

if __name__ == '__main__':
    questions = ["Which of the following is correct for any random variables A and B?",
    "What is equal to the average number of customers in any M/M/1 queue, in which new arrivals occur at rate λ according to a Poisson process, and service times are exponentially distributed with rate μ? [Note: ρ = λ/μ]",
    "What is the probability that a M/M/1 queue is empty, in which new arrivals occur at rate λ according to a Poisson process, and service times are exponentially distributed with rate μ? [Note: ρ = λ/μ]",
    "What is the probability that the stationary process of a M/M/1 queue, in which new arrivals occur at rate λ according to a Poisson process, and service times are exponentially distributed with rate μ, is in the state 'i' (a.k.a. currently has i customers)? [Note: ρ = λ/μ]",
    "A M/M/1 queue, in which new arrivals occur at rate λ according to a Poisson process, and service times are exponentially distributed with rate μ, is considered as STABLE if...? [Note: ρ = λ/μ]",
    "In a M/M/1 queue, in which new arrivals occur at rate λ according to a Poisson process, and service times are exponentially distributed with rate μ, what is the mean service time equal to? [Note: ρ = λ/μ]",
    "In a M/M/1 queue, in which new arrivals occur at rate λ according to a Poisson process, and service times are exponentially distributed with rate μ, the ratio ρ = λ / μ, is also referred to as...?",
    "What is the average time spent waiting in a M/M/1 queue, in which new arrivals occur at rate λ according to a Poisson process, and service times are exponentially distributed with rate μ? [Note: ρ = λ/μ]",
    "In Queue Theory, as 'mean service time' we define...?"]    
    answers = [["P(A|B) = P(B|A) * P(A) / P(B)", "P(A|B) = P(B|A) * P(B) / P(A)", "P(A|B) = P(A|B) * P(A) / P(B)", "P(A|B) = P(B|A) * P(AB) / P(B)"],
    ["ρ/(1-ρ)", "μ/(λ-μ)", "λ/(λ-μ)", "ρ/(λ-μ)"],
    ["1-ρ","(1-ρ)/2", "ρ/(1-ρ)", "1/ρ(μ-λ)"],
    ["(1-ρ)*ρ^i","(1-ρ)^i","1/ρ^i", "ρ^i/(1-ρ)"],
    ["λ < μ", "μ < λ", "ρ < μ", "ρ < λ"],
    ["1/μ", "1/λ", "ρ/(μ+λ)", "1/ρ"],
    ["Utilization factor", "Traffic intensity", "Service rate", "Service time"],
    ["ρ/(μ-λ)", "ρ/(λ-μ)", "μ/(ρ-λ)", "μ/(λ-ρ)"],
    ["The average time spent once a customer starts being served until the completition of the service", "The average time spent once a customer enters the system until the completition of the service", "The average time spent once a customer starts being served until the beginning of the service", "The average time spent once a customer enters the system until the completition of the service of all the customers that arrived later"]]
    questions_right_answers = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # Shuffle the order of the questions
    questions, answers, questions_right_answers = shuffle_questions_with_answers(questions, answers, questions_right_answers)
    # Shuffle the order of the answers
    for i in range(len(answers)):
        answers[i], questions_right_answers[i] = shuffle_answer_order(answers[i], questions_right_answers, i)
    app = QApplication(sys.argv)
    game = QuizGame(questions, answers, questions_right_answers)
    game.show()
    sys.exit(app.exec())