from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

app = Flask(__name__)

@app.route('/dados', methods=['POST'])
def verificar_login_instagram():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email e senha são obrigatórios.'}), 400

    try:
        isLoggedIn = fazer_login_instagram(email, password)
        if isLoggedIn:
            return 'Login válido!'
        else:
            return 'Credenciais inválidas.', 401
    except Exception as e:
        return f'Ocorreu um erro: {str(e)}', 500

def fazer_login_instagram(email, password):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(options=chrome_options)

    try:
        browser.get('https://www.instagram.com/accounts/login/')
        
        # Esperar até que o campo de email esteja presente
        email_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]'))
        )
        # Esperar até que o campo de senha esteja presente
        password_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="password"]'))
        )
        
        email_input.send_keys(email)
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        # Esperar até que a página seja carregada após o login
        WebDriverWait(browser, 10).until(
            EC.url_changes('https://www.instagram.com/accounts/login/')
        )

        if 'login' not in browser.current_url:
            return True
        else:
            return False
    finally:
        browser.quit()

if __name__ == '__main__':
    app.run(debug=True)
