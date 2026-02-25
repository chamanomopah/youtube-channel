from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests
import time

url = "https://readcomiconline.li/Comic/Absolute-Batman/Issue-1?id=234426"

options = Options()
# options.add_argument("--headless")  # Descomente depois de testar
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get(url)
wait = WebDriverWait(driver, 15)

# Espere a página carregar
time.sleep(3)

# Tente clicar no Server 1
try:
    server_btns = driver.find_elements(By.XPATH, "//a[contains(text(), 'Server')]")
    if server_btns:
        server_btns[0].click()
        time.sleep(1)
except:
    pass

# Tente clicar em High Quality
try:
    quality_btns = driver.find_elements(By.XPATH, "//a[contains(text(), 'High') or contains(text(), 'Quality')]")
    if quality_btns:
        quality_btns[0].click()
        time.sleep(2)
except:
    pass

os.makedirs("pages", exist_ok=True)

page_num = 1
max_pages = 100  # Limite de segurança
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Referer': 'https://readcomiconline.li/'
}

print("Iniciando download das paginas...")

while page_num <= max_pages:
    # Espere a imagem carregar
    time.sleep(2)

    # Encontre a imagem do comic (URLs do blogspot)
    all_images = driver.find_elements(By.TAG_NAME, "img")
    comic_img = None

    for img in all_images:
        src = img.get_attribute("src") or ""
        # Procure por imagens do blogspot que sejam grandes
        if "blogspot.com" in src or "bp.blogspot.com" in src:
            try:
                if img.size['width'] > 300:  # Imagem grande
                    comic_img = src
                    break
            except:
                pass

    if not comic_img:
        print(f"Página {page_num}: Não encontrou imagem")
        break

    # Baixe a imagem
    try:
        print(f"Baixando página {page_num}: {comic_img[:70]}...")
        img_data = requests.get(comic_img, headers=headers, timeout=15).content

        # Verifique se não é uma imagem de erro
        if len(img_data) < 10000:  # Muito pequena, provavelmente erro
            print(f"  -> Imagem muito pequena ({len(img_data)} bytes), pode ser erro")
            # Continue anyway para ver

        ext = ".jpg"
        if ".png" in comic_img:
            ext = ".png"
        elif ".webp" in comic_img:
            ext = ".webp"

        filename = f"pages/page_{page_num:03d}{ext}"
        with open(filename, "wb") as f:
            f.write(img_data)

        # Verifique se já baixamos esta imagem antes (pode ser a última página)
        if page_num > 1:
            prev_file = f"pages/page_{page_num-1:03d}{ext}"
            if os.path.exists(prev_file):
                with open(prev_file, "rb") as f:
                    prev_data = f.read()
                if img_data == prev_data:
                    print(f"  -> Imagem repetida! Fim das páginas.")
                    break

    except Exception as e:
        print(f"  -> Erro ao baixar: {e}")

    # Clique em "Next" para ir para a próxima página
    try:
        next_btn = driver.find_element(By.ID, "btnNext")
        if next_btn:
            # Verifique se o botão está desabilitado (fim do comic)
            class_attr = next_btn.get_attribute("class") or ""
            style = next_btn.get_attribute("style") or ""

            # Se o botão estiver desabilitado ou oculto, paramos
            if "disabled" in class_attr or "display: none" in style or "display:none" in style:
                print(f"\nBotão Next desabilitado. Fim do comic!")
                break

            next_btn.click()
            page_num += 1
        else:
            print("\nNão encontrou botão Next")
            break
    except Exception as e:
        print(f"\nErro ao clicar em Next: {e}")
        break

driver.quit()
print(f"\nDownload concluído! {page_num} páginas baixadas em 'pages/'")
