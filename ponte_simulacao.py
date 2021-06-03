# A única biblioteca externa utilizada foi a pyglet, que foi feita para renderizar gráficos 
import pyglet 
from pyglet.window import key

#Cria a janela
win = pyglet.window.Window(650, 350)
win.set_caption("Simulação de Ponte Hidráulica")

#Inicia o sistema de input do usuário
keys = key.KeyStateHandler() 
win.push_handlers(keys)

#Variaveis responsaveis por renderizar o desenho da ponte
batch = pyglet.graphics.Batch() 
pistoes = pyglet.graphics.Batch()
textos = pyglet.graphics.Batch()

#O que está sendo feito a baixo é um processo de criar formatos na tela, foi usado alguns blocos para desenhar a ponte
chapa = pyglet.shapes.Rectangle(20, 172, 200, 15, (255, 255, 255), batch=batch)
chapa.anchor_x = 15
chapa.anchor_y = 7
chapa2 = pyglet.shapes.Rectangle(395, 172, 200, 15, (255, 255, 255), batch=batch)
chapa2.anchor_x = 185
chapa2.anchor_y = 7
base = pyglet.shapes.Rectangle(10, 10, 30, 199, (255, 255, 255), batch=batch)
base2 = pyglet.shapes.Rectangle(375, 10, 30, 199, (255, 255, 255), batch=batch)
pistao = pyglet.shapes.Line(40, 30, 100, 100, 1, (255, 0 , 0), batch=pistoes)
pistao2 = pyglet.shapes.Line(375, 30, 100, 100, 1, (255, 0 , 0), batch=pistoes)

#Variaveis
velocidade = 10 #velocidade angular da ponnte
angulo_max = 45 #o maior angulo que a ponte pode rotacionar
angulo_min = 0 #o menor angulo que a ponte pode rotacionar

# Para desenhar os pistoes, foi utilizado duas coordenadas para cada ponta, 
# estas variaveis são as coordenadas que especificam aonde eles devem estar
pistao.x2 = 200-56 
pistao.y2 = 172-(15/2)
pistao2.x2 = 215+56
pistao2.y2 = 172-(15/2)

altura_pistao = 18 #altura do pistão em cm
forca_vertical = 0.98 #a força vertical, em newtons, que o pistão possui

#Desenha o texto na tela como output para o usuário 
tamanho_pistoes = pyglet.text.Label('Altura do pistão: ', font_name='Calibri', font_size=13, x=420, y=310, batch=textos)
volume = pyglet.text.Label('Volume do pistão: ', font_name='Calibri', font_size=13, x=420, y=290, batch=textos)
force = pyglet.text.Label('Força vertical: ', font_name='Calibri', font_size=13, x=420, y=270, batch=textos)
massa = pyglet.text.Label('Carga máxima: ', font_name='Calibri', font_size=13, x=420, y=250, batch=textos)

#Lógica de loop
def update(dt):
    global altura_pistao
    volume_valor = (altura_pistao - 18)*(3.1415*(1**2))*2.2 #calcula o volume do pistão 
    forca_vertical = (((pistao.y2-12)/10)/altura_pistao)*0.98 #calcula a força vertical
    if volume_valor < 0: 
        volume_valor = 0

    #Atualiza os textos da tela para a visualização do usuário
    volume.text = 'Volume do pistão: {:.2f} cm³'.format(volume_valor)
    tamanho_pistoes.text = 'Altura do pistão: {:.2f} cm'.format(altura_pistao)
    force.text = 'Força vertical: {:.2f} N'.format(forca_vertical)
    massa.text = 'Torque do pistão: {:.2f} N/m'.format(forca_vertical*0.13)

    #Caso o usuário aperte a tecla para cima, o pistão ira aumentar a altura e as chapas iram rotacionar
    #Caso a tecla para baixo seja pressionada, o oposto irá acontecer
    if keys[key.UP] and chapa2.rotation < angulo_max:
        chapa.rotation -= velocidade * dt
        chapa2.rotation += velocidade * dt
        pistao.x2 -= velocidade * dt
        pistao2.x2 += velocidade * dt
        pistao.y2 += velocidade * dt * 2
        pistao2.y2 += velocidade * dt * 2
        altura_pistao += 1.507 * dt
    elif keys[key.DOWN] and chapa2.rotation > angulo_min:
        chapa.rotation += velocidade * dt
        chapa2.rotation -= velocidade * dt
        pistao.x2 += velocidade * dt
        pistao2.x2 -= velocidade * dt
        pistao.y2 -= velocidade * dt * 2
        pistao2.y2 -= velocidade * dt * 2
        altura_pistao -= 1.507 * dt

#Renderização
@win.event
def on_draw():
    win.clear()
    pistoes.draw()
    batch.draw()
    textos.draw()

#Final
pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()