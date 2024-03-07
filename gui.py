import tkinter as tk
from tkinter import ttk
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def on_close():
    main_window.destroy()

def doswiadczenie_wybranie_jezyka(event):
    wybrany_jezyk = doswiadczenieComboBox.get()
    doswiadczenieSlider.set(jezyki_dosw[wybrany_jezyk])

def update_doswiadczenie(event):
    wybrany_jezyk = doswiadczenieComboBox.get()
    jezyki_dosw[wybrany_jezyk] = doswiadczenieSlider.get()

def get_rules(jezyk, trudnosc, zlozonosc_skladni, doswiadczenie, jezyk_dopasowanie):
    if jezyk == 'HTML' or jezyk == 'CSS' or jezyk == 'SQL' or jezyk == 'Python' or jezyk == 'Julia' \
        or jezyk == 'MATLAB' or jezyk == 'SAS' or jezyk == 'Go' or jezyk == 'Lua' or jezyk == 'Swift':  # niska trudnosc niska zlozonosc
        rule1 = ctrl.Rule(trudnosc['l'] & zlozonosc_skladni['l'], jezyk_dopasowanie['vh'])
        rule2 = ctrl.Rule(trudnosc['m'] | zlozonosc_skladni['m'], jezyk_dopasowanie['m'])
        rule3 = ctrl.Rule(trudnosc['h'] | zlozonosc_skladni['h'], jezyk_dopasowanie['vl'])
        rule4 = ctrl.Rule(doswiadczenie['h'], jezyk_dopasowanie['h'])
        rule5 = ctrl.Rule(doswiadczenie['m'], jezyk_dopasowanie['m'])
        rule6 = ctrl.Rule(doswiadczenie['l'], jezyk_dopasowanie['l'])
        rule7 = ctrl.Rule(trudnosc['h'] & zlozonosc_skladni['h'] & doswiadczenie['l'], jezyk_dopasowanie['vl'])
    elif jezyk == 'JavaScript' or jezyk == 'TypeScript' or jezyk == 'Ruby' or jezyk == 'Objective-C' \
        or jezyk == 'Dart' or jezyk == 'Flutter' or jezyk == 'React Native' or jezyk == 'PHP' or jezyk == 'Ada':  # srednia trudnosc srednia zlozonosc?
        rule1 = ctrl.Rule(trudnosc['m'] & zlozonosc_skladni['m'], jezyk_dopasowanie['vh'])
        rule2 = ctrl.Rule(trudnosc['h'] | zlozonosc_skladni['l'], jezyk_dopasowanie['m'])
        rule3 = ctrl.Rule(trudnosc['l'] | zlozonosc_skladni['h'], jezyk_dopasowanie['m'])
        rule4 = ctrl.Rule(doswiadczenie['h'], jezyk_dopasowanie['h'])
        rule5 = ctrl.Rule(doswiadczenie['m'], jezyk_dopasowanie['m'])
        rule6 = ctrl.Rule(doswiadczenie['l'], jezyk_dopasowanie['l'])
        rule7 = ctrl.Rule(trudnosc['l'] & zlozonosc_skladni['h'] & doswiadczenie['l'], jezyk_dopasowanie['vl'])
    elif jezyk == 'Java' or jezyk == 'C#' or jezyk == 'Kotlin' or jezyk == 'Angular' or jezyk == 'Rust':  # srednia trudnosc wysoka skladnia
        rule1 = ctrl.Rule(trudnosc['m'] & zlozonosc_skladni['h'], jezyk_dopasowanie['vh'])
        rule2 = ctrl.Rule(trudnosc['h'] | zlozonosc_skladni['m'], jezyk_dopasowanie['h'])
        rule3 = ctrl.Rule(trudnosc['l'] | zlozonosc_skladni['l'], jezyk_dopasowanie['l'])
        rule4 = ctrl.Rule(doswiadczenie['h'], jezyk_dopasowanie['h'])
        rule5 = ctrl.Rule(doswiadczenie['m'], jezyk_dopasowanie['m'])
        rule6 = ctrl.Rule(doswiadczenie['l'], jezyk_dopasowanie['l'])
        rule7 = ctrl.Rule(trudnosc['l'] & zlozonosc_skladni['l'] & doswiadczenie['l'], jezyk_dopasowanie['vl'])
    elif jezyk == 'Perl' or jezyk == 'Assembler' or jezyk == 'Haskell':
        rule1 = ctrl.Rule(trudnosc['h'] & zlozonosc_skladni['h'], jezyk_dopasowanie['vh'])
        rule2 = ctrl.Rule(trudnosc['m'] | zlozonosc_skladni['m'] | zlozonosc_skladni['h'], jezyk_dopasowanie['m'])
        rule3 = ctrl.Rule(trudnosc['l'] | zlozonosc_skladni['l'], jezyk_dopasowanie['vl'])
        rule4 = ctrl.Rule(doswiadczenie['h'], jezyk_dopasowanie['h'])
        rule5 = ctrl.Rule(doswiadczenie['m'], jezyk_dopasowanie['m'])
        rule6 = ctrl.Rule(doswiadczenie['l'], jezyk_dopasowanie['l'])
        rule7 = ctrl.Rule(trudnosc['l'] & zlozonosc_skladni['l'] & doswiadczenie['l'], jezyk_dopasowanie['vl'])
    elif jezyk == 'C++' or jezyk == 'C' or jezyk == 'R' or jezyk == 'Scala':  #tu duza trudnosc
        rule1 = ctrl.Rule(trudnosc['h'] & zlozonosc_skladni['m'], jezyk_dopasowanie['vh'])
        rule2 = ctrl.Rule(trudnosc['m'] | zlozonosc_skladni['h'], jezyk_dopasowanie['h'])
        rule3 = ctrl.Rule(trudnosc['l'] | zlozonosc_skladni['m'] | zlozonosc_skladni['l'], jezyk_dopasowanie['l'])
        rule4 = ctrl.Rule(doswiadczenie['h'], jezyk_dopasowanie['h'])
        rule5 = ctrl.Rule(doswiadczenie['m'], jezyk_dopasowanie['m'])
        rule6 = ctrl.Rule(doswiadczenie['l'], jezyk_dopasowanie['l'])
        rule7 = ctrl.Rule(trudnosc['l'] & zlozonosc_skladni['l'] & doswiadczenie['l'], jezyk_dopasowanie['vl'])

    return [rule1, rule2, rule3, rule4, rule5, rule6, rule7]

def oblicz_rozmyte(suma, wyniki, wym_do_rozwazenia):
    final_scores = {}

    for jezyk, ocena in suma.items():
        doswiadczenie = ctrl.Antecedent(np.arange(0, 101, 1), 'doswiadczenie')
        trudnosc = ctrl.Antecedent(np.arange(0, 101, 1), 'trudnosc')
        zlozonosc_skladni = ctrl.Antecedent(np.arange(0, 101, 1), 'zlozonosc_skladni')
        jezyk_dopasowanie = ctrl.Consequent(np.arange(0, 101, 1), jezyk)

        trudnosc.automf(5, names=['l', 'm', 'h'])  # Automatyczne podziałki dla popularności
        zlozonosc_skladni.automf(5, names=['l', 'm', 'h'])  # Automatyczne podziałki dla złożoności składni
        doswiadczenie.automf(5, names=['l', 'm', 'h'])  # Automatyczne podziałki dla złożoności składni

        jezyk_dopasowanie['vl'] = fuzz.trimf(jezyk_dopasowanie.universe, [0, 0, 10])
        jezyk_dopasowanie['l'] = fuzz.trimf(jezyk_dopasowanie.universe, [10, 30, 50])
        jezyk_dopasowanie['m'] = fuzz.trimf(jezyk_dopasowanie.universe, [30, 50, 70])
        jezyk_dopasowanie['h'] = fuzz.trimf(jezyk_dopasowanie.universe, [50, 70, 90])
        jezyk_dopasowanie['vh'] = fuzz.trimf(jezyk_dopasowanie.universe, [90, 100, 100])

        system_rozmyty = ctrl.ControlSystem(get_rules(jezyk, trudnosc, zlozonosc_skladni, doswiadczenie, jezyk_dopasowanie))
        system = ctrl.ControlSystemSimulation(system_rozmyty)

        system.input['trudnosc'] = trudnoscSlider.get()  # Przykładowe preferencje popularności
        system.input['zlozonosc_skladni'] = skladniaSlider.get()  # Przykładowe preferencje złożoności składni
        system.input['doswiadczenie'] = jezyki_dosw[jezyk]  # Przykładowe preferencje złożoności składni

        system.compute()

        system_wynik = system.output[jezyk] / 10 #wynik systemu rozmytego w skali 0 - 10
        srednia_wynik = (wyniki[jezyk] + suma[jezyk]) / 2 #srednia z ocen rodzaju projektu i wymagan

        if len(wym_do_rozwazenia) != 0:
            final_scores[jezyk] = (system_wynik + srednia_wynik) / 2
        else:
            final_scores[jezyk] = system_wynik

    return final_scores
def wygeneruj_jezyki():
    rodzaj_projektu = rodzajProjektuComboBox.get()
    jezyki_do_zachowania = rodzaje_projektu_baza[rodzaj_projektu].keys() #jezyki ktore zostaly po wykluczeniu
    wyniki = rodzaje_projektu_baza[rodzaj_projektu].copy()
    wymagania_z_gui = []
    suma = {} #suma punktow z wymagan

    for i in range(len(wymaganiaCheckBoxesVars)): #pobierz wymagania z checkboxow
        if wymaganiaCheckBoxesVars[i].get():
            wymagania_z_gui.append(wymaganiaCheckBoxes[i].cget("text"))

    for key in wyniki:
        suma[key] = 0

    #wymagania ktore zostaly zaznaczone wraz z lista jezykow ktore trzeba rozwazyc i ich ocenami
    wym_do_rozwazenia = {
        kategoria: {
            jezyk: wymagania_baza[kategoria][jezyk]
            for jezyk in jezyki_do_zachowania
        }
        for kategoria in wymagania_z_gui
    }

    #obliczenie sumy wartosci jezykow dla kazdego wymgania
    for wymaganie, jezyki in wym_do_rozwazenia.items():
        for jezyk, ocena in jezyki.items():
            suma[jezyk] += ocena * 0.2 * (5 / (len(wym_do_rozwazenia))) #musi sie sumowac do 10

    #uwzględnij preferencje
    final_scores = oblicz_rozmyte(suma, wyniki, wym_do_rozwazenia)

    final_scores_sorted = dict(sorted(final_scores.items(), key=lambda x: x[1], reverse=True))
    final_scores_list = list(final_scores_sorted.items())
    result_text = 'Lista języków:\n'
    for i in range(5):
        result_text += f"{i+1}. {final_scores_list[i][0]} - {final_scores_list[i][1]:.2f}\n"

    wynikLabel.config(text=result_text)
    wynikLabel.grid(row=3, column=1)

#bazy wiedzy
jezyki_dosw = {"HTML": 0, "CSS": 0, "JavaScript": 0, "Python": 0, "PHP": 0, "Ruby": 0, "Java": 0, "C#": 0,
               "TypeScript": 0, "Kotlin": 0, "Perl": 0, "Rust": 0, "Angular": 0, "Swift": 0, "Objective-C": 0,
               "C++": 0, "Dart": 0, "C": 0, "R": 0, "SQL": 0, "Julia": 0, "Scala": 0, "MATLAB": 0, "SAS": 0,
               "Assembler": 0, "Go": 0, "Ada": 0, "Lua": 0, "React Native": 0, "Flutter": 0, 'Haskell': 0}

rodzaje_projektu_baza = {
    "Strona Internetowa": {'HTML': 10, 'CSS': 10, 'JavaScript': 10, 'Python': 8, "PHP": 7, 'Ruby': 6, 'Java': 8,
                           'C#': 8, 'TypeScript': 9, 'Kotlin': 8, 'Perl': 5, 'Rust': 6, 'Angular': 9},
    "Aplikacja Mobilna": {'Java': 10, 'Kotlin': 10, 'Swift': 10, 'Objective-C': 6, 'C#': 7, 'React Native': 8,
                          'Flutter': 7, 'Rust': 6, 'Angular': 6},
    "Aplikacja Desktopowa": {'Java': 9, 'C#': 9, 'Python': 7, "C++": 8, 'Swift': 8, 'Ruby': 6, 'Rust': 6, 'Dart': 7,
                             'C': 4},
    "Analiza Danych": {'Python': 10, 'R': 9, 'SQL': 8, 'Julia': 7, 'Scala': 8, 'MATLAB': 7, 'SAS': 7, 'Perl': 6,
                       'Haskell': 7},
    "System Wbudowany": {'C': 10, 'C++': 9, 'Assembler': 8, 'Python': 7, 'Java': 6, 'Rust': 8, 'Ada': 7, 'Go': 7,
                         'Swift': 7},
    "Gra Komputerowa": {'C++': 10, 'C#': 10, 'JavaScript': 8, 'Python': 6, 'Lua': 5, 'Rust': 7, 'TypeScript': 8,
                        'Ruby': 5}
}
wymagania_baza = {
    "Wydajność": {
        "HTML": 3, "CSS": 3, "JavaScript": 6, "Python": 7, "PHP": 4, "Ruby": 5, "Java": 8, "C#": 8,
        "TypeScript": 8, "Kotlin": 8, "Perl": 4, "Rust": 9, "Angular": 6, "Swift": 8, "Objective-C": 7,
        "C++": 10, "Dart": 5, "C": 10, "R": 4, "SQL": 5, "Julia": 6, "Scala": 7, "MATLAB": 6, "SAS": 5,
        "Assembler": 10, "Go": 8, "Ada": 7, "Lua": 4, "React Native": 6, "Flutter": 5, 'Haskell': 7
    },
    "Skalowalność": {
        "HTML": 3, "CSS": 3, "JavaScript": 7, "Python": 7, "PHP": 3, "Ruby": 5, "Java": 10  , "C#": 9,
        "TypeScript": 7, "Kotlin": 7, "Perl": 3, "Rust": 8, "Angular": 6, "Swift": 7, "Objective-C": 6,
        "C++": 7, "Dart": 5, "C": 7, "R": 5, "SQL": 6, "Julia": 5, "Scala": 7, "MATLAB": 6, "SAS": 5,
        "Assembler": 4, "Go": 9, "Ada": 6, "Lua": 3, "React Native": 5, "Flutter": 6, 'Haskell': 5
    },
    "Wieloplatformowość": {
        "HTML": 10, "CSS": 10, "JavaScript": 10, "Python": 8, "PHP": 6, "Ruby": 6, "Java": 9, "C#": 9,
        "TypeScript": 8, "Kotlin": 8, "Perl": 5, "Rust": 8, "Angular": 7, "Swift": 7, "Objective-C": 7,
        "C++": 7, "Dart": 6, "C": 8, "R": 5, "SQL": 6, "Julia": 5, "Scala": 7, "MATLAB": 5, "SAS": 5,
        "Assembler": 4, "Go": 8, "Ada": 7, "Lua": 5, "React Native": 6, "Flutter": 6, 'Haskell': 6
    },
    "Bezpieczeństwo": {
        "HTML": 8, "CSS": 8, "JavaScript": 6, "Python": 7, "PHP": 4, "Ruby": 6, "Java": 7, "C#": 7,
        "TypeScript": 6, "Kotlin": 6, "Perl": 5, "Rust": 9, "Angular": 6, "Swift": 7, "Objective-C": 6,
        "C++": 7, "Dart": 5, "C": 7, "R": 5, "SQL": 7, "Julia": 5, "Scala": 6, "MATLAB": 5, "SAS": 5,
        "Assembler": 6, "Go": 7, "Ada": 6, "Lua": 5, "React Native": 6, "Flutter": 6, 'Haskell': 9
    },
    "Popularność": {
        "HTML": 9, "CSS": 9, "JavaScript": 10, "Python": 10, "PHP": 7, "Ruby": 6, "Java": 9, "C#": 8,
        "TypeScript": 8, "Kotlin": 7, "Perl": 4, "Rust": 8, "Angular": 6, "Swift": 6, "Objective-C": 4,
        "C++": 7, "Dart": 6, "C": 7, "R": 5, "SQL": 9, "Julia": 4, "Scala": 4, "MATLAB": 5, "SAS": 2,
        "Assembler": 6, "Go": 7, "Ada": 3, "Lua": 6, "React Native": 7, "Flutter": 7, 'Haskell': 4
    }
}

main_window = tk.Tk()
main_window.title("Placing elements in Tk")
main_window.attributes("-fullscreen", True)

tytulLabel = tk.Label(text="WYBÓR OPTYMALNEGO JĘZYKA PROGRAMOWANIA", font=('Helvetica', 34))
tytulLabel.grid(row=0, column=0, columnspan=3, pady=10)

bottomLeftFrame = tk.Frame()
bottomLeftFrame.grid(row=2, column=0, sticky="en")
bottomRightFrame = tk.Frame()
bottomRightFrame.grid(row=2, column=2, sticky="wn")
topFrame = tk.Frame()
topFrame.grid(row=1, column=1)

rodzajProjektuLabel = tk.Label(topFrame, text="Wybierz rodzaj projektu", font=('Helvetica', 12))
rodzajProjektuLabel.grid(row=0, column=0)
stringvar_projekt = tk.StringVar()
rodzajProjektuComboBox = ttk.Combobox(topFrame, textvariable=stringvar_projekt, font=('Helvetica', 12))
rodzajProjektuComboBox['values'] = ( 'Strona Internetowa', 'Aplikacja Mobilna', 'Aplikacja Desktopowa',
                                     "Gra Komputerowa", "Analiza Danych", "System Wbudowany")
rodzajProjektuComboBox['state'] = 'readonly'
rodzajProjektuComboBox.grid(row=0, column=1)

doswiadczenieFrame = tk.Frame()
doswiadczenieFrame.grid(row=3, column=2, sticky="wn")

doswiadczenieComboBox = ttk.Combobox(doswiadczenieFrame, width=12, textvariable=tk.StringVar(), font=('Helvetica', 12))
doswiadczenieComboBox['values'] = ("HTML", "CSS", "JavaScript", "Python", "PHP", "Ruby", "Java", "C#",
                                   "TypeScript", "Kotlin", "Perl", "Rust", "Angular", "Swift", "Objective-C",
                                   "C++", "Dart", "C", "R", "SQL", "Julia", "Scala", "MATLAB", "SAS",
                                   "Assembler", "Go", "Ada", "Lua", "React Native", "Flutter", 'Haskell')
doswiadczenieComboBox['state'] = 'readonly'
doswiadczenieComboBox.grid(row=1, column=0)
doswiadczenieComboBox.set('HTML')

doswiadczenieComboBox.bind("<<ComboboxSelected>>", doswiadczenie_wybranie_jezyka)

doswiadczenieLabel = tk.Label(doswiadczenieFrame, text="Doswiadczenie", font=('Helvetica', 12))
doswiadczenieLabel.grid(row=0, column=0, sticky=tk.W)

doswiadczenieSlider = ttk.Scale(doswiadczenieFrame, from_=0, to=100, orient="horizontal", length=100)
doswiadczenieSlider.grid(row=1, column=1, sticky=tk.W, padx=10)
doswiadczenieSlider.bind("<Motion>", update_doswiadczenie)
doswiadczenieSlider.set(1)  # Ustawienie wartości domyślnej

wymaganiaLabel = tk.Label(bottomLeftFrame, text="Wybierz wymagania", font=('Helvetica', 12))
wymaganiaLabel.grid(row=0, column=0)

preferencjeLabel = tk.Label(bottomRightFrame, text="Wybierz preferencje", font=('Helvetica', 12))
preferencjeLabel.grid(row=0, column=0)

wymagania = ['Skalowalność', 'Wydajność', 'Bezpieczeństwo', 'Wieloplatformowość', 'Popularność']
wymaganiaCheckBoxes = []
wymaganiaCheckBoxesVars = []

#stworz checkboxy z wymaganiami
for i, wymaganie in enumerate(wymagania):
    boolVar = tk.BooleanVar()
    checkbutton = tk.Checkbutton(bottomLeftFrame, text=wymaganie, variable=boolVar)
    checkbutton.grid(row=i + 1, column=0, sticky=tk.W)
    wymaganiaCheckBoxes.append(checkbutton)
    wymaganiaCheckBoxesVars.append(boolVar)

generujButton = tk.Button(text="Generuj Jezyki", font=('Helvetica', 24), command=wygeneruj_jezyki)
generujButton.grid(row=2, column=1, padx=10)

wynikLabel = tk.Label(font=('Helvetica', 16), justify='left')

trudnoscLabel = tk.Label(bottomRightFrame, text="Trudność języka")
trudnoscLabel.grid(row=1, column=0, sticky=tk.W)
trudnoscSlider = ttk.Scale(bottomRightFrame, from_=0, to=100, orient="horizontal", length=100)
trudnoscSlider.grid(row=1, column=1, sticky=tk.W)
trudnoscSlider.set(2)  # Ustawienie wartości domyślnej

skladniaLabel = tk.Label(bottomRightFrame, text="Złożoność składni")
skladniaLabel.grid(row=2, column=0, sticky=tk.W)
skladniaSlider = ttk.Scale(bottomRightFrame, from_=0, to=100, orient="horizontal", length=100)
skladniaSlider.grid(row=2, column=1, sticky=tk.W)
skladniaSlider.set(2)  # Ustawienie wartości domyślnej

exitButton = tk.Button(text="Wyjście", font=('Helvetica', 16), command=on_close)
exitButton.grid(row=4, column=1, padx=10)

main_window.columnconfigure(0, weight=2)
main_window.columnconfigure(1, weight=2)
main_window.columnconfigure(2, weight=1)
main_window.rowconfigure(0, weight=1)
main_window.rowconfigure(1, weight=1)
main_window.rowconfigure(2, weight=1)
main_window.rowconfigure(3, weight=1)
main_window.rowconfigure(4, weight=12)
main_window.rowconfigure(5, weight=3)

main_window.mainloop()