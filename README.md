# 🛌 Drowsiness Detection System

<!-- <p align="center">
  <img src="[URL_DO_SEU_GIF_OU_SCREENSHOT_AQUI]" alt="Demonstração do Face Mesh em tempo real" width="700"/>
</p> -->

Este projeto é uma ferramenta de segurança baseada em **Visão Computacional** e **Inteligência Artificial**. O sistema monitoriza o estado de vigília do utilizador através da análise de marcos faciais, sendo capaz de detetar sinais de fadiga e disparar alertas sonoros para prevenção de acidentes.

---

## 🚀 Key Features

* **Deteção Facial Avançada:** Mapeamento de 468 pontos (Face Mesh) com alta precisão.
* **Monitorização Ocular:** Análise em tempo real do estado das pálpebras.
* **Alerta de Segurança:** Lógica integrada para disparar alarmes em caso de sonolência prolongada (> 1.5s).
* **Alta Performance:** Desenvolvido para rodar com baixo consumo de recursos e alto FPS.

---

## 🏗️ Lógica de Funcionamento

O sistema utiliza a biblioteca **MediaPipe** para processar a malha facial e extrair os marcos (landmarks) dos olhos. Através do cálculo do **Eye Aspect Ratio (EAR)**, o software identifica se o rácio de abertura ocular está abaixo do limiar de segurança.



---

## 🛠️ Tech Stack

* [Python 3.11](https://www.python.org/)
* [OpenCV](https://opencv.org/)
* [MediaPipe](https://mediapipe.dev/)
* [Pygame](https://www.pygame.org/) (Gestão de áudio em tempo real)

---

## ▶️ Guia de Instalação e Uso

> [!CAUTION]
> **Requisito Obrigatório:** Este projeto foi desenvolvido e testado exclusivamente no **Python 3.11**. Versões superiores ou inferiores podem apresentar instabilidades nas dependências do MediaPipe.

<details>
  <summary><strong>Clique para ver o passo a passo (Dev Setup)</strong></summary>

Siga as instruções abaixo para configurar o ambiente e executar o projeto localmente.

### 1. Preparar o Ambiente
```bash
# Clone o repositório (O Git criará a pasta FaceMeshProject automaticamente)
git clone https://github.com/tenoriopedro/FaceMeshProject.git
```

### 2. Configurar Ambiente Virtual (VENV)
```bash

# Criar o ambiente
python -m venv venv

# Ativar no Windows:
.\venv\Scripts\activate

# Ativar no Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependências
```bash

pip install -r requirements.txt
```

### 4. Executar
```bash

python face_mesh.py
```

</details>


## 🔮 Roadmap e Melhorias Futuras

Este projeto é um MVP (*Minimum Viable Product*) funcional. O plano de desenvolvimento futuro visa transformar este protótipo num produto robusto para uso em cenário real de condução.

- [ ] **Calibração Automática de Sensibilidade:**
    - Implementar uma fase inicial de 5 segundos para medir o EAR "normal" do utilizador e ajustar o limiar (Threshold) dinamicamente, evitando falsos positivos em pessoas com olhos naturalmente mais fechados.

- [ ] **Deteção de Bocejos (Yawn Detection):**
    - Integrar o cálculo do *Mouth Aspect Ratio (MAR)* para identificar bocejos repetitivos como um sinal precoce de fadiga, antes mesmo do fecho ocular.

- [ ] **Análise de Postura da Cabeça (Head Pose):**
    - Utilizar a geometria 3D do MediaPipe para detetar o "cabecear" (queda brusca da cabeça para a frente), cobrindo situações onde o condutor adormece sem fechar totalmente os olhos.

- [ ] **Modo Noturno (Infravermelhos):**
    - Adaptação do algoritmo para processar imagens de câmaras IR (Infravermelhas), permitindo o funcionamento em ambientes de escuridão total (habitáculo do carro à noite).

- [ ] **Registo de Dados (Data Logging):**
    - Criação de um sistema de logs que exporta um relatório `.csv` com os horários e duração dos eventos de sonolência para análise posterior.

- [ ] **Portabilidade (Embedded Systems):**
    - Otimização do código para execução em *Edge Devices* como Raspberry Pi 4 ou NVIDIA Jetson Nano.