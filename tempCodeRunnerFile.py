import tkinter as tk
from tkinter import ttk
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random

### ===== Funções Comuns =====

def create_driver():
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

def human_delay(min_sec=1.0, max_sec=2.5):
    time.sleep(random.uniform(min_sec, max_sec))

def human_click(element):
    human_delay(0.3, 1.2)
    element.click()
    human_delay(0.8, 2.5)

def check_capture(driver):
    try:
        modal = driver.find_element(By.CLASS_NAME, "modarrest")
        if "capturado" in modal.text.lower():
            print("Capturado! Tentando subornar...")
            btn = driver.find_element(By.CSS_SELECTOR, "input[name='cop[paymax]']")
            human_click(btn)
            return True
    except:
        pass
    return False

def get_stamina(driver):
    try:
        return int(driver.find_element(By.CSS_SELECTOR, "a[title*='Estamina:'] u").text.strip())
    except:
        return 0

def recover_stamina(driver):
    try:
        stamina_element = driver.find_element(By.CSS_SELECTOR, "a.smarttip[title*='Estamina:']")
        human_click(stamina_element)
        time.sleep(3)
        if check_capture(driver): return False
        item = driver.find_element(By.CSS_SELECTOR, "img.item_small[src*='505.jpg']")
        human_click(item)
        return not check_capture(driver)
    except:
        return False

def check_toxicity(driver):
    try:
        tox_element = driver.find_element(By.CSS_SELECTOR, "a[title*='Intoxicação:'] u")
        toxicity = int(tox_element.text.strip())
        if toxicity > 120:
            human_click(tox_element)
            human_delay(4, 5)
            for _ in range(10):
                try:
                    detox_btn = driver.find_element(By.CSS_SELECTOR, "a.hospital_detox")
                    human_click(detox_btn)
                    break
                except:
                    time.sleep(1)
    except:
        pass

### ===== Scripts =====

def prender(driver):
    while True:
        for page_num in range(1, 10):
            base_url = f"https://reidocrime.com/top10/user///{page_num}/"
            driver.get(base_url)
            human_delay(2, 3)
            if check_capture(driver): continue

            for row in range(2, 32):
                try:
                    driver.get(base_url)
                    human_delay(1, 2)
                    if check_capture(driver): break

                    xpath = f"//div[@id='cwrapper']/div[3]/div[3]/div/div/div/div/div/table/tbody/tr[{row}]/td[2]/a"
                    element = driver.find_element(By.XPATH, xpath)
                    human_click(element)

                    if check_capture(driver): break
                    if get_stamina(driver) < 50:
                        if not recover_stamina(driver): continue

                    links = driver.find_elements(By.CLASS_NAME, "smarttip")
                    for link in links:
                        if "prender" in link.text.lower() or "fiscal" in link.text.lower():
                            human_click(link)
                            time.sleep(2)
                            try:
                                confirm_btn = driver.find_element(By.CSS_SELECTOR, "input[name='no-bribe']")
                                human_click(confirm_btn)
                                break
                            except:
                                pass
                except:
                    pass

def atacar(driver):
    def get_valores():
        try:
            vida = int(driver.find_element(By.CSS_SELECTOR, "a[title*='Vida:'] u").text.strip())
            estamina = int(driver.find_element(By.CSS_SELECTOR, "a[title*='Estamina:'] u").text.strip())
            return vida, estamina
        except:
            return 0, 0

    def get_risk():
        try:
            return int(driver.find_element(By.CSS_SELECTOR, "a[title*='Risco:'] u").text.strip())
        except:
            return 0

    def recover_life():
        try:
            driver.get("https://reidocrime.com/top10/fight?z=jav")
            human_delay()
            if check_capture(driver): return False
            item = driver.find_element(By.CSS_SELECTOR, "img.item_small[src*='804.jpg']")
            item.click()
            return not check_capture(driver)
        except:
            return False

    def reduce_risk():
        try:
            driver.get("https://reidocrime.com/top10/fight?z=jav")
            human_delay()
            if check_capture(driver): return False
            item = driver.find_element(By.CSS_SELECTOR, "img.item_small[src*='806.jpg']")
            item.click()
            return not check_capture(driver)
        except:
            return False

    while True:
        driver.get("https://reidocrime.com/top10/fight")
        time.sleep(3)
        check_capture(driver)

        vida, estamina = get_valores()
        if vida < 20:
            recover_life()
        if estamina < 50:
            recover_stamina(driver)
        if get_risk() > 330:
            reduce_risk()
        check_toxicity(driver)

        try:
            attack_btns = driver.find_elements(By.CLASS_NAME, "beat")
            if attack_btns:
                human_click(attack_btns[0])
        except:
            pass

def atacar_agente(driver):
    def attack_agent_js():
        js_code = '''
            const agentLink = document.querySelector("a.spot.agent");
            if (agentLink) {
              agentLink.click();
              setTimeout(() => {
                const attackLink = document.querySelector("a.st[href*='agent.attack']");
                if (attackLink) {
                  attackLink.click();
                }
              }, 1500);
            }
        '''
        driver.execute_script(js_code)

    while True:
        for page_num in range(1, 10):
            base_url = f"https://reidocrime.com/top10/user///{page_num}/"
            driver.get(base_url)
            time.sleep(2)
            if check_capture(driver): continue

            check_toxicity(driver)
            if get_stamina(driver) < 50:
                if not recover_stamina(driver): continue

            for row in range(2, 32):
                try:
                    driver.get(base_url)
                    time.sleep(1)
                    if check_capture(driver): break

                    xpath = f"//div[@id='cwrapper']/div[3]/div[3]/div/div/div/div/div/table/tbody/tr[{row}]/td[2]/a"
                    element = driver.find_element(By.XPATH, xpath)
                    human_click(element)

                    if check_capture(driver): break
                    attack_agent_js()
                    time.sleep(4)
                except:
                    pass

### ===== Interface Gráfica =====

def iniciar_interface():
    driver = None

    def iniciar_driver():
        nonlocal driver
        if driver is None:
            driver = create_driver()
            driver.get("https://reidocrime.com/")
            print("Aguardando login por 60 segundos...")
            time.sleep(60)

    def rodar(func):
        def wrapper():
            iniciar_driver()
            func(driver)
        Thread(target=wrapper, daemon=True).start()

    root = tk.Tk()
    root.title("Rei do Crime Trainer - OneThinker")
    root.geometry("450x300")

    tab_control = ttk.Notebook(root)

    aba_acao = ttk.Frame(tab_control)
    aba_tutoriais = ttk.Frame(tab_control)
    aba_creditos = ttk.Frame(tab_control)

    tab_control.add(aba_acao, text='Ações')
    tab_control.add(aba_tutoriais, text='Tutoriais')
    tab_control.add(aba_creditos, text='Créditos')

    tab_control.pack(expand=1, fill='both')

    ttk.Label(aba_acao, text="Escolha uma ação para executar:").pack(pady=10)
    ttk.Button(aba_acao, text="Prender", command=lambda: rodar(prender)).pack(pady=5)
    ttk.Button(aba_acao, text="Atacar", command=lambda: rodar(atacar)).pack(pady=5)
    ttk.Button(aba_acao, text="Atacar Agentes", command=lambda: rodar(atacar_agente)).pack(pady=5)

    ttk.Label(aba_tutoriais, text="Instruções de uso:", font=('Arial', 11, 'bold')).pack(pady=10)
    tutorial = (
        "• Você tem 60 segundos para logar após iniciar.\n"
        "• Para usar o modo 'Prender', você precisa ser um detetive.\n"
        "• Para usar 'Atacar', vá em 'Encontrar uma briga'\n"
        "   e defina os níveis e respeito antes de iniciar.\n"
        "• Scripts rodam automaticamente em loop.\n"
    )
    ttk.Label(aba_tutoriais, text=tutorial, wraplength=420, justify='left').pack(padx=10)

    tk.Label(aba_creditos, text="Criado por:", font=('Arial', 12)).pack(pady=10)
    tk.Label(aba_creditos, text="Discord: OneThinker", font=('Arial', 10, 'bold')).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()
