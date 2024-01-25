import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.remote.webdriver import By
from time import sleep
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import openpyxl
from datetime import datetime

driver = uc.Chrome()
driver.get('https://blaze-4.com/pt/games/double')
sleep(5)

loopTrue = 1
greens_seguidos = 0
wins = 0
loses = 0
brancos = 0
entradas = 0
greens = 0
reds = 0
win = f'✅✅✅✅✅✅✅✅'
win_branco = '⬜ Green do branco ⬜'
loss = '❌❌❌❌❌❌❌❌❌'

def SalvarLucroDia():
    global wins
    global loses
    global greens
    global reds
    global brancos
    global entradas

    book = openpyxl.load_workbook('Planilha de Lucros.xlsx')
    lucros_page = book['Lucro']
    lucros_page.append([datetime.now().strftime("%d/%m/%Y"),str(round(wins - loses,2)),greens+reds,brancos,greens,reds])
    book.save('Planilha de Lucros.xlsx')
    print("Lucro do dia salvo!")

    

def resetar_marcadores():
    global wins
    global loses12
    global greens
    global reds
    global brancos
    global entradas

    wins = 0
    loses = 0
    brancos = 0
    entradas = 0
    greens = 0
    reds = 0

def martin_gale(gale,ultimo):
    global wins
    global brancos
    enviar_mensagem(gale)
    esperar()
    sleep(1.5)
    ultimo_ = retornar_ultimo()
    if ultimo_ != ultimo and ultimo_ != 0:
        enviar_mensagem(win)
        wins += 0.4
        return True    
    elif ultimo_ == 0: 
        enviar_mensagem(win_branco)
        brancos += 1
        wins += 2
        return True
def esperar():
    while True:
        try:
            driver.find_element(By.CLASS_NAME,'time-left').find_element(By.TAG_NAME,'span').text
            break
        except:
            pass
    while True:
        try:
            driver.find_element(By.CLASS_NAME,'time-left').find_element(By.TAG_NAME,'span').text
        except:
            break
        
def retornar_historico():
    return [i['color'] for i in requests.get('https://blaze-4.com/api/roulette_games/recent').json()][::-1]

def retornar_ultimo():
    return requests.get('https://blaze-4.com/api/roulette_games/current').json()['color']
            
def enviar_mensagem(mensagem):
    bot_token = '6720302766:AAHyO4-HdPmF5_Pkdf9CGkz7ULt8J9O6GKc'
    chat_id = '-1002042459876'
    url_blaze = '🎰 [Blaze](https://blaze-4.com/pt/games/double)'
    if 'Entrada' in mensagem and 'não' not in mensagem:
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={mensagem}\n{url_blaze}&parse_mode=Markdown'
    else:
        url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={mensagem}'
    requests.get(url)

def enviar_mensagem_contador():
    contador = f'\n✅ Greens: {round(wins,2)}u\n❌ Reds: {round(loses,2)}u'
    if wins - loses >= 0:
        contador += f'\n✅ Total: {round(wins-loses,2)}u'
    else:
        contador += f'\n❌ Total: {round(wins-loses,2)}u'
    enviar_mensagem(contador)


def contar_greens_seguidos():
    global greens_seguidos
    global wins
    global loses
    global loopTrue
    if wins - loses >= 3:
        enviar_mensagem("Stop win batido!!\nAté amanhã")
        SalvarLucroDia()
        loopTrue = 1
    elif loses - wins >= 3.6:
        enviar_mensagem("Stop loss batido!!\nAté amanhã")
        SalvarLucroDia()
        loopTrue = 1
    elif greens_seguidos == 3:
        enviar_mensagem("Vamos fazer uma pausa para evitar reds")
        sleep(3600)
        greens_seguidos = 0
    else:
        greens_seguidos += 1

def IniciarAnalises():
    global loopTrue
    loopTrue = 0
    enviar_mensagem("Iniciando as análises do dia")

def funcaoPausada():
    while loopTrue != 0:
        pass
    return

scheduler = BackgroundScheduler()
scheduler.add_job(IniciarAnalises, 'cron', hour=10, minute=00)
scheduler.start()
cor = ['Branco','Preto','Vermelho']
simbolo = ['⬜','⬛','🟥']
funcaoPausada()
while loopTrue == 0:
    try:
        print('ok')
        esperar()
        sleep(1.5)
        historico = retornar_historico()
        ultimo = retornar_ultimo()
        historico.append(ultimo)
        padrao = historico[-4:]
        print(padrao)
        confirmacao = f'{simbolo[padrao[0]]} Entrada confirmada no {cor[padrao[0]]} (1u)\n{simbolo[0]} Proteção no Branco (0,2u)'
        gale1 = f'Vamos para o gale 1 \n{simbolo[padrao[0]]} {cor[padrao[0]]} (2u)\n{simbolo[0]} Proteção no Branco (0,4u)'
        
        #Como as estratégias sempre jogam na cor contraria, resolvi colocar as cores
        #Vermelha e Preta em indices diferentes para aproveirar a logica
        if padrao == [1,1,1,1] or padrao == [2,2,2,2] or padrao == [1,2,1,2] or padrao == [2,1,2,1]:                
            esperar()
            sleep(1.5)
            ultimo = retornar_ultimo()
            while True:
                if ultimo == padrao[0]:
                    enviar_mensagem(confirmacao)
                    esperar()
                    sleep(1.5)
                    ultimo_ = retornar_ultimo()
                    if ultimo_ != ultimo and ultimo_ != 0:
                        wins += 0.8
                        greens +=1
                        enviar_mensagem(win)
                        contar_greens_seguidos()
                    elif ultimo_ == 0:
                        wins += 1.6
                        greens +=1
                        enviar_mensagem(win)
                        sleep(2)
                        enviar_mensagem(win_branco)
                        contar_greens_seguidos()
                    else:
                        if not martin_gale(gale1,ultimo):
                            loses += 3.6
                            reds += 1
                            enviar_mensagem(loss)
                            greens_seguidos = 0
                        else:
                            greens += 1
                            contar_greens_seguidos()
                    enviar_mensagem_contador()
                    break    
                break
    except Exception as e:
        print(e)
        driver.get('https://blaze-4.com/pt/games/double')
        sleep(10)
        pass

resetar_marcadores()