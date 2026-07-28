from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    """Главная страница"""
    return render_template('index.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    """Страница калькулятора"""
    result = None
    error = None
    
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            num1 = float(request.form.get('num1'))
            num2 = float(request.form.get('num2'))
            operation = request.form.get('operation')

            # Выполняем операцию
            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                if num2 == 0:
                    error = "Ошибка: Деление на ноль!"
                else:
                    result = num1 / num2
            else:
                error = "Неизвестная операция"
                
        except ValueError:
            error = "Ошибка: Пожалуйста, введите корректные числа."
        except Exception as e:
            error = f"Произошла ошибка: {str(e)}"

    return render_template('calculator.html', result=result, error=error)

if __name__ == '__main__':
    app.run(debug=True)