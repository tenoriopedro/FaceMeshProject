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

* [Python](https://www.python.org/)
* [OpenCV](https://opencv.org/)
* [MediaPipe](https://mediapipe.dev/)
* [Pygame](https://www.pygame.org/) (Gestão de áudio em tempo real)

---

## ▶️ Guia de Instalação e Uso

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

python main.py
```

</details>