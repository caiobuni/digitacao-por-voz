# Verbatim 🎙️✨

**Verbatim** é um aplicativo de ditado inteligente e invisível para Windows, projetado para transformar sua fala em texto perfeitamente pontuado e escrito, direto onde o seu cursor estiver. Inspirado em ferramentas modernas de produtividade, ele roda discretamente na bandeja do sistema (system tray) e é ativado por um simples atalho de teclado.

## 🎯 Proposta

A digitação por voz tradicional muitas vezes entrega textos sem pontuação, com palavras mal interpretadas ou exige que você abra janelas separadas para ditar e depois copiar/colar. 

O objetivo do Verbatim é oferecer uma experiência **imediata e fluida**: você segura uma tecla, fala naturalmente, e o texto aparece magicamente no seu e-mail, código, documento do Word ou chat de WhatsApp, já formatado corretamente graças à inteligência artificial.

## ⚙️ Como Funciona

 O Verbatim utiliza três pilares principais para seu funcionamento:
 
1. **Atalho Global Silencioso**: Configuramos a tecla `Pause/Break` como o gatilho principal. Por ser uma tecla sem função na maioria dos editores de texto modernos, ela não suja a sua tela com caracteres indesejados enquanto você a segura.
2. **Transcrição de Alta Precisão (Whisper V3 via Groq)**: Ao soltar a tecla (ou após uma breve pausa na sua fala - VAD), o áudio é enviado para a API ultra-rápida do Groq utilizando o modelo open-source `whisper-large-v3`. O sistema envia "contextos de pontuação" para a IA, obrigando-a a devolver o texto com gramática e pontuação impecáveis, ignorando ruídos e silêncios puros (temperatura 0.0) para não alucinar textos inexistentes.
3. **Escrita Mágica**: A resposta da transcrição é jogada na sua área de transferência e colada no seu cursor ativo instantaneamente simulando um `Ctrl+V`. Logo em seguida, a sua área de transferência original é restaurada para você não perder links ou textos copiados anteriormente.

Além disso, todas as suas transcrições ficam guardadas localmente num log de histórico (`transcriptions.md`), acessível direto pelo ícone azul com um "V" perto do seu relógio do Windows.

## 💸 Tempo de Uso Gratuito e Custos (Groq API)

O Verbatim foi construído para ser utilizado com a **API do Groq**, que atualmente possui uma das mais generosas cotas gratuitas do mercado para processamento de áudio (Hardware LPUs). 

Com a conta **Free/Gratuita**, na data atual de criação do nosso projeto, seus limites diários abrangem:
- **Até 2.000 requisições (frases enviadas) por dia.**
- **Aproximadamente 8 horas de envio de áudio líquido (28.800 segundos) por dia.**

**O que isso significa na prática?**
Como ditamos textos com pausas para formular frases e ler o contexto (uma frase ativa média dura cerca de 5 a 10 segundos no aplicativo), esses limites contemplam facilmente entre **2 a 3 horas de "fala contínua ininterrupta"** todos os dias. 

Para a imensa maioria dos usuários e rotinas de trabalho regulares (responder e-mails, rascunhar relatórios, escrever mensagens e códigos), a cota gratuita provida pelo Groq é virtualmente **ilimitada**, oferecendo tecnologia de ponta sem custo algum para o seu dia a dia.

---

## 🚀 Guia Rápido de Instalação e Execução

### Pré-requisitos
- Ter o Python instalado no seu Windows.
- Criar uma conta no [Groq Console](https://console.groq.com/) e gerar uma **API Key**.

### Passos
1. Clone este repositório: `git clone https://github.com/seunome/verbatim.git`
2. Crie a sua chave de API do Groq e coloque na raiz do projeto dentro de um arquivo chamado `.env`:
   ```env
   GROQ_API_KEY="gsk_sua_chave_aqui"
   ```
3. Crie seu ambiente virtual e instale os requerimentos:
   ```powershell
   python -m venv venv
   .\venv\Scripts\python -m pip install -r requirements.txt
   ```
4. Para rodar: `.\venv\Scripts\python main.py`
5. Para configurar a auto-inicialização oculta com o Windows: `.\venv\Scripts\python startup.py`

**Aproveite seu novo assistente de ditado!**
