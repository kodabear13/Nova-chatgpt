# imports
import openai
import speech_recognition as sr
from tkinter.constants import DISABLED, NORMAL
import tkinter as tk
from datetime import datetime

from tkinter import ttk
#from tkinter import messagebox

now = datetime.now()
current_time = now.strftime("%H:%M")


# Set up OpenAI API credentials
openai.api_key = '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'

def ask_openai(question):
    model_engine = "text-davinci-003"
    prompt = f"Q: {question}\nA:"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    message = completions.choices[0].text.strip()
    return message

# Function to recognize speech using microphone
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand you."
    except sr.RequestError:
        return "Sorry, my speech recognition service is currently down."


def clear_entry(event, entry):
    entry.delete(0, 'end')
    entry.unbind('<Button-1>', event)        
# Creating a window called self.window
class ChatbotGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Nova")
        self.window.geometry("600x600")
        self.window.configure(bg='black')

        # Creating a self scroll frame
        self.scroll_frame = tk.Frame(self.window)
        self.scroll_frame.pack(side="top", fill="both", expand=True)

        self.chat_history = tk.Text(self.scroll_frame, wrap="word", state="disabled")
        self.chat_history.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.scroll_frame, orient="vertical", command=self.chat_history.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.chat_history.configure(yscrollcommand=self.scrollbar.set, bg="cyan")
        
        self.question_entry = tk.Entry(self.window, width=200, font=("Courier", 20), bg="black", fg="turquoise")
        self.question_entry.pack(pady=15, padx=15)
        self.window.bind('<Return>', self.ask_question)

        placeholder_text = 'Saisissez un message ici.'
        self.question_entry.insert(0, placeholder_text)
        self.question_entry.bind("<Button-1>", lambda event: clear_entry(event, self.question_entry))

        self.ask_button = tk.Button(self.window, text="Demander", width=200,  command=self.ask_question, font=("Courier", 20, 'bold'), fg="blue",)
        self.ask_button.pack(pady=15, padx=15)

        self.clear_button = tk.Button(self.window, text="Clair", width=200, command=self.clear_all, font=("Courier", 20, 'bold'), fg="navy")
        self.clear_button.pack(pady=15, padx=15)

        self.listen_button = tk.Button(self.window, text="Parler",width=200, command=self.listen_question, font=("Courier", 20, 'bold'), fg="red")
        self.listen_button.pack(pady=15, padx=15)
        self.window.mainloop()
        
    def clear_all(self):
        self.chat_history.configure(state="normal")
        self.chat_history.delete("1.0", tk.END)
        self.chat_history.configure(state="disabled")

    def ask_question(self, event):
        question = self.question_entry.get().strip()
        if question != "":
            response = ask_openai(question)
            self.update_chat_history(question, response)

    def listen_question(self):
        question = recognize_speech()
        self.question_entry.delete(0, tk.END)
        self.question_entry.insert(0, question)
        response = ask_openai(question)
        self.update_chat_history(question, response)

    def update_chat_history(self, question, response):
        self.chat_history.configure(state="normal")
        if self.chat_history.index('end') != None:
            self.chat_history.insert('end',current_time+' ', ("small", "right", "white"))
            self.chat_history.window_create('end', window=tk.Label(self.chat_history, fg="white",
            text=question,
            wraplength=200, font=("Arial", 18), bg="#218aff", bd=4, justify="left"))
            self.chat_history.insert('end','\n\n ', "left")
            self.chat_history.insert('end',current_time+' ', ("small", "left", "white"))
            self.chat_history.window_create('end', window=tk.Label(self.chat_history, fg="blue",
            text=response,
            wraplength=200, font=("Arial", 18), bg="#aeb9cc", bd=4, justify="right"))
            self.chat_history.insert('end','\n\n ', "right")
            self.chat_history.tag_configure("right", justify="right")
            self.chat_history.tag_configure(foreground="gold", font=("Arial", 12, 'bold'))
            self.chat_history.configure(state="disabled")
            self.chat_history.yview('end')

if __name__ == "__main__":
    gui = ChatbotGUI()
