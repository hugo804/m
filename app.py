from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

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
    chrome_options.add_argument("--no-sandbox")  # Adicione esta opção

    browser = webdriver.Chrome(options=chrome_options)

    try:
        browser.get('https://www.instagram.com/accounts/login/')
        
        email_input = browser.find_element_by_css_selector('input[name="username"]')
        password_input = browser.find_element_by_css_selector('input[name="password"]')
        
        email_input.send_keys(email)
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

        browser.implicitly_wait(10)

        if 'login' not in browser.current_url:
            return True
        else:
            return False
    finally:
        browser.quit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')