#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Модуль Игры
# Базовый набор для игр

class WrongChoiceError(Exception):
    pass

class Player(object):
    """Участник игры"""
    def __init(self, name, score = 0):
        self.name = name
        self.score = score

    def __str__(self):
        rep = self.name + ":\t" + str(self.score)
        return rep

def ask_yes_no(question):
    """Задает вопрос с ответом 'да' или 'нет'."""
    response = None
    while response not in ("y", "n"):
        response = input(question).lower()
    return response
    
def ask_number(question, low, high):
    """Просит ввести число из заданного диапазона"""
    while True:
        try:
            response = int(input(question))
            if response not in range(low, high):
                print("Число вне указанного диапазона")
                continue
            break
        except ValueError:
            print("Ввести можно только число.")
    return response

if __name__ == "__main__":
    print("Вы запустили этот модуль напрямую, а не импортировали его.")
    input("\n\nНажмите Enter, чтобы выйти.")
    
