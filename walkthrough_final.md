# Verbatim: Walkthrough & Guia de Uso

O **Verbatim** agora está totalmente funcional e pronto para uso no seu Windows!

## O que foi implementado
- [x] **Gravação por Atalho**: Segure a tecla `Pause/Break` para falar.
- [x] **Detecção de Silêncio (VAD)**: Se você fizer uma pausa de 0.8s, o sistema já transcreve e digita a frase, mesmo com a tecla pressionada. Além disso, silêncios absolutos são ignorados para evitar "alucinações" do modelo.
- [x] **Transcrição Inteligente**: Usa Groq Whisper V3 com um prompt que garante pontuação e ortografia excelentes.
- [x] **Digitação Automática**: O texto aparece onde o cursor estiver, preservando sua área de transferência original.
- [x] **Fundo e Tray**: Ícone na bandeja do sistema com menu para abrir o histórico ou sair.
- [x] **Auto-inicialização**: Script para configurar a abertura automática com o Windows.

## Estrutura do Projeto
- `main.py`: O coração do app, integra tudo.
- `recorder.py`: Captura áudio e filtra silêncios vazios.
- `transcriber.py`: Envia para o Groq (com temperatura 0.0 para reduzir alucinações) e recebe o texto corrigido.
- `typer.py`: Realiza a "mágica" de colar o texto na tela.
- `logger.py`: Salva tudo em `transcriptions.md`.
- `tray.py`: Cria o ícone perto do relógio.
- `startup.py`: Configura o app para iniciar com o Windows.

## Como Usar

### 1. Iniciar o App manualmente
No terminal, dentro da pasta do projeto, execute:
```powershell
.\venv\Scripts\python main.py
```
Você verá um ícone azul com um "V" na sua bandeja do sistema.

### 2. Configurar Inicialização com o Windows
Para que o app abra sozinho sempre que você ligar o computador (e sem aparecer janelas pretas), execute:
```powershell
.\venv\Scripts\python startup.py
```
Isso criará um atalho na sua pasta `Startup` do Windows que roda o app de forma oculta.

### 3. Usando o Atalho de Voz
1. Abra qualquer programa de texto (Bloco de Notas, Word, WhatsApp Web, etc.).
2. Clique no local onde deseja escrever.
3. **Segure** a tecla `Pause` (ou `Pause/Break`) no seu teclado.
4. Comece a falar.
   - Se você parar por um instante, o que você disse será digitado automaticamente.
   - Continue falando se quiser.
5. **Solte** a tecla para finalizar a última parte da fala.

### 4. Consultar Histórico
Clique com o botão direito no ícone do Verbatim na bandeja e selecione **"Abrir Histórico"**. O arquivo `transcriptions.md` será aberto.

---
**Dica**: A tecla `Pause/Break` é ideal pois ela praticamente não tem nenhuma outra função em campos de texto no Windows, garantindo que o seu cursor não seja "sujo" com espaços, pipes ou abas enquanto você grava.
