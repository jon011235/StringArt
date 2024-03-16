# Implementierungsschritte

1) Anti-Aliasing
- Male eine gerade Linie von links nach rechts
- Male eine Diagonale
- Male eine vertikale Linie
- Merke dir was für ein Fehler zwischen dem gesetzten Pixel und dem von der Linie gewünschten Punkt ist.

2) Vertraut machen mit dem Rest des Framework
 - Implementieren von ```printOperations```
 - Zeichne ein Quadrat in das Bild ein
 - finde die dunkelste Linie von Nagel 0 aus

3) Greedy
i = Nagel 0. 
Ziehe die dunkelste Linie die von Nagel i aus möglich ist. 
Der Nagel an dem die Linie endet ist der neue Nagel i

4) Wie könnte man den Algorithmus verbessern?
Mögliche Ansätze:
- anderes Anti-aliasing (xiaolin Wu)
- Vorberechnen aller möglichen Linien (falls Nagel 0 sehr ungeeignet ist)
- berechnen der verwendeten Fadenlänge
- Kein Greedy Algorithmus (priority Queue, Fast Fourier Transformations)
