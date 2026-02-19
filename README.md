# Open-source Image Compressor

## 🇬🇧 English

A simple and efficient tool to compress and optimize images (JPEG, PNG, HEIC) with a user-friendly dark-themed GUI built with `customtkinter`.

### Purpose
This project enables users to quickly reduce image file sizes without requiring technical knowledge. Perfect for freeing up disk space or preparing images for web upload.

### Features
- Dark-themed GUI using `customtkinter`
- Multiple file selection (JPG, JPEG, PNG, HEIC)
- Compression slider (1-10, where 10 = maximum compression)
- Progress bar with estimated time remaining
- Output saved to `compressed` folder alongside original files

### Getting Started (Windows / PowerShell)

#### 1) Create and activate a virtual environment (recommended)

Open PowerShell in the project directory and run:

```powershell
# Create virtual environment (one time only)
python -m venv .\venv

# Activate virtual environment (PowerShell)
.\venv\Scripts\Activate
```

After activation, your prompt should display `(venv)` at the beginning.

#### 2) Install dependencies from `requirements.txt`

With the virtual environment active, run:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3) Run the application

With the environment active and dependencies installed:

```powershell
python main.py
```

#### 4) Using the interface

- Click `Select Images` and choose your files (JPG, JPEG, PNG, HEIC)
- Adjust the slider to select compression level (1-10)
- Click `Compress` to start the process
- Compressed images will be saved in the `compressed` folder

### Notes and Recommendations
- **HEIC support**: Uses `pillow-heif` library (converts HEIC to JPG before compression)
- **PNG compression**: Utilizes Pillow with paletized mode (`P`) conversion for maximum compression without external binaries
- **PNG optimization**: For even more aggressive PNG compression, install `optipng` externally (requires Windows executable)

### License
Open-source project for personal use and educational purposes.

---

## 🇧🇷 Português Brasileiro

Uma ferramenta simples e eficiente para comprimir e otimizar imagens (JPEG, PNG, HEIC) com uma interface gráfica amigável com tema escuro construída em `customtkinter`.

### Objetivo
O projeto permite que usuários reduzam rapidamente o tamanho dos arquivos de imagem sem exigir conhecimento técnico. Perfeito para liberar espaço em disco ou preparar imagens para upload na web.

### Recursos
- Interface gráfica com tema escuro usando `customtkinter`
- Seleção múltipla de arquivos (JPG, JPEG, PNG, HEIC)
- Slider de compressão (1-10, onde 10 = máxima compressão)
- Barra de progresso com tempo estimado restante
- Saída salva em pasta `compressed` ao lado dos arquivos originais

### Como Começar (Windows / PowerShell)

#### 1) Criar e ativar um ambiente virtual (recomendado)

Abra o PowerShell no diretório do projeto e execute:

```powershell
# Cria o ambiente virtual (apenas uma vez)
python -m venv .\venv

# Ativa o ambiente virtual (PowerShell)
.\venv\Scripts\Activate
```

Após a ativação, seu prompt deve exibir `(venv)` no início.

#### 2) Instalar dependências do `requirements.txt`

Com o ambiente virtual ativo, execute:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3) Executar a aplicação

Com o ambiente ativo e dependências instaladas:

```powershell
python main.py
```

#### 4) Usando a interface

- Clique em `Select Images` e escolha seus arquivos (JPG, JPEG, PNG, HEIC)
- Ajuste o slider para selecionar o nível de compressão (1-10)
- Clique em `Compress` para iniciar o processo
- As imagens comprimidas serão salvas na pasta `compressed`

### Notas e Recomendações
- **Suporte HEIC**: Utiliza biblioteca `pillow-heif` (converte HEIC para JPG antes da compressão)
- **Compressão PNG**: Usa Pillow com conversão de modo paletizado (`P`) para máxima compressão sem binários externos
- **Otimização PNG**: Para compressão PNG ainda mais agressiva, instale `optipng` externamente (requer executável Windows)

### Licença
Projeto open-source para uso pessoal e fins educacionais.
