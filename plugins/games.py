import random
from typing import Dict

class GamesPlugin:
    def __init__(self):
        self.trivia_questions = [
            {'question': 'What is the capital of France?', 'answer': 'Paris', 'options': ['London', 'Paris', 'Berlin', 'Madrid']},
            {'question': 'What is 15 × 7?', 'answer': '105', 'options': ['95', '105', '115', '125']},
            {'question': 'Who wrote "1984"?', 'answer': 'George Orwell', 'options': ['Aldous Huxley', 'George Orwell', 'Ray Bradbury', 'Isaac Asimov']}
        ]
        
        self.riddles = [
            {'riddle': 'I speak without a mouth and hear without ears. I have no body, but come alive with wind. What am I?', 'answer': 'An echo'},
            {'riddle': 'The more you take, the more you leave behind. What am I?', 'answer': 'Footsteps'},
            {'riddle': 'What has keys but no locks, space but no room, and you can enter but not go inside?', 'answer': 'A keyboard'}
        ]
        
        self.active_games: Dict[str, Dict] = {}
    
    async def start_trivia(self, user_id: str) -> tuple:
        question = random.choice(self.trivia_questions)
        self.active_games[user_id] = {'type': 'trivia', 'question': question}
        random.shuffle(question['options'])
        text = f"🎯 **Trivia Time!**\n\n{question['question']}"
        return text, question['options']
    
    async def check_trivia_answer(self, user_id: str, answer: str) -> str:
        if user_id not in self.active_games:
            return "❌ No active trivia game. Use /trivia to start!"
        game = self.active_games[user_id]
        correct = game['question']['answer']
        del self.active_games[user_id]
        if answer == correct:
            return f"✅ Correct! The answer is **{correct}**!"
        else:
            return f"❌ Wrong! The correct answer was **{correct}**"
    
    async def get_riddle(self, user_id: str) -> str:
        riddle = random.choice(self.riddles)
        self.active_games[user_id] = {'type': 'riddle', 'riddle': riddle}
        return f"🤔 **Riddle:**\n\n{riddle['riddle']}\n\nType your answer!"
    
    async def check_riddle_answer(self, user_id: str, answer: str) -> str:
        if user_id not in self.active_games or self.active_games[user_id]['type'] != 'riddle':
            return None
        game = self.active_games[user_id]
        correct = game['riddle']['answer'].lower()
        if answer.lower() in correct or correct in answer.lower():
            del self.active_games[user_id]
            return f"✅ Correct! The answer is **{game['riddle']['answer']}**!"
        return None
    
    async def math_challenge(self) -> tuple:
        a = random.randint(10, 50)
        b = random.randint(10, 50)
        op = random.choice(['+', '-', '×'])
        if op == '+':
            answer = str(a + b)
            question = f"{a} + {b}"
        elif op == '-':
            answer = str(a - b)
            question = f"{a} - {b}"
        else:
            answer = str(a * b)
            question = f"{a} × {b}"
        return f"🧮 **Math Challenge:**\n\n{question} = ?", answer
